"""MCP protocol tests use synthetic documents; these are not live OAuth evidence."""
import asyncio
import json
import os
import sys
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from drive_api import APIError
from server import build_server
import server


class FakeAPI:
    def __init__(self):
        self.write_ids = {'doc1'}
        self.text = 'Deadline: October 15.\n'
        self.revision = 'revision1'
        self.writes = 0

    def search(self, *args):
        return {'documents': [{'doc_id': 'doc1', 'title': 'Project Schedule'}],
                'next_page_token': None, 'incomplete_search': False}

    def document(self, doc_id):
        if doc_id != 'doc1':
            raise APIError('NOT_FOUND_OR_NO_ACCESS', 'Not found.', 'Search again for a valid doc_id.')
        return {'title': 'Project Schedule', 'revisionId': self.revision,
                'tabs': [{'tabProperties': {'tabId': 't.0', 'title': 'Main'},
                          'documentTab': {'body': {'content': [{'paragraph': {
                              'elements': [{'textRun': {'content': self.text}}]}}]}}}]}

    def apply(self, doc_id, tab_id, old, new, revision):
        assert revision == self.revision
        self.writes += 1
        count = self.text.count(old)
        self.text = self.text.replace(old, new)
        self.revision = 'revision2'
        return {'replies': [{'replaceAllText': {'occurrencesChanged': count}}]}


def run(coro):
    return asyncio.run(coro)


def data(result):
    return result.structured_content


def error_data(result):
    # ToolError payload is carried in MCP content with isError=true.
    return json.loads(result.content[0].text)


def test_protocol_chain_preview_apply_and_replay():
    async def scenario():
        api = FakeAPI()
        async with Client(build_server(api)) as client:
            tools = {tool.name: tool for tool in await client.list_tools()}
            assert len(tools) == 4
            assert all(t.inputSchema.get('additionalProperties') is False for t in tools.values())
            assert tools['read_document'].annotations.readOnlyHint
            assert not tools['apply_document_update'].annotations.readOnlyHint
            assert tools['search_documents'].inputSchema['properties']['scope']['enum'] == ['accessible', 'shared_with_me', 'owned_by_me']
            search = data(await client.call_tool('search_documents', {'keyword': 'Schedule'}))
            doc_id = search['documents'][0]['doc_id']
            read = data(await client.call_tool('read_document', {'doc_id': doc_id}))
            preview = data(await client.call_tool('preview_document_update', dict(doc_id=doc_id,
                tab_id=read['tabs'][0]['tab_id'], old_text='October 15', new_text='October 20')))
            assert api.writes == 0
            applied = data(await client.call_tool('apply_document_update', {'preview_id': preview['preview_id']}))
            assert applied['readback_verified'] and api.writes == 1
            replay = await client.call_tool('apply_document_update', {'preview_id': preview['preview_id']}, raise_on_error=False)
            assert replay.is_error and error_data(replay)['error'] == 'PREVIEW_EXPIRED_OR_UNKNOWN'
            assert api.writes == 1
    run(scenario())


def test_protocol_revision_conflict_prevents_write():
    async def scenario():
        api = FakeAPI()
        async with Client(build_server(api)) as client:
            preview = data(await client.call_tool('preview_document_update', dict(doc_id='doc1', tab_id='t.0', old_text='October 15', new_text='October 20')))
            api.revision = 'collaborator-revision'
            result = await client.call_tool('apply_document_update', {'preview_id': preview['preview_id']}, raise_on_error=False)
            assert error_data(result)['error'] == 'REVISION_CONFLICT'
            assert api.writes == 0
    run(scenario())


@pytest.mark.parametrize('arguments', [
    {'keyword':'x', 'scope':'calendar'}, {'keyword':'x', 'page_size':51}, {'keyword':''},
    {'keyword':'x', 'page_size':'10'}, {'keyword':'x', 'unexpected_argument':True}])
def test_protocol_invalid_schema(arguments):
    async def scenario():
        api = FakeAPI()
        async with Client(build_server(api)) as client:
            result = await client.call_tool('search_documents', arguments, raise_on_error=False)
            assert result.is_error
            assert api.writes == 0
    run(scenario())


@pytest.mark.parametrize('old,new,expected', [
    ('October 15', 'October 15 revised', True),
    ('October 15', '', True),
    ('October 15', 'October 20', False)])
def test_protocol_readback_checks_exact_expected_tab(old, new, expected):
    async def scenario():
        api = FakeAPI()
        if not expected:
            # The new phrase already exists elsewhere: substring presence proves nothing.
            api.text += 'Other event: October 20.\n'
            def misleading_apply(*args):
                api.writes += 1
                return {'replies': [{'replaceAllText': {'occurrencesChanged': 1}}]}
            api.apply = misleading_apply
        async with Client(build_server(api)) as client:
            preview = data(await client.call_tool('preview_document_update', dict(
                doc_id='doc1', tab_id='t.0', old_text=old, new_text=new)))
            result = data(await client.call_tool('apply_document_update', {'preview_id':preview['preview_id']}))
            assert result['readback_verified'] is expected
            assert result['status'] == ('applied' if expected else 'applied_readback_mismatch')
            assert api.writes == 1
    run(scenario())


def test_protocol_expired_preview_does_not_write(monkeypatch):
    async def scenario():
        api = FakeAPI()
        clock = [1000.0]
        monkeypatch.setattr(server.time, 'monotonic', lambda: clock[0])
        async with Client(build_server(api)) as client:
            preview = data(await client.call_tool('preview_document_update', dict(
                doc_id='doc1', tab_id='t.0', old_text='October 15', new_text='October 20')))
            clock[0] += 601
            result = await client.call_tool('apply_document_update', {'preview_id':preview['preview_id']}, raise_on_error=False)
            assert error_data(result)['error'] == 'PREVIEW_EXPIRED_OR_UNKNOWN'
            assert api.writes == 0
    run(scenario())


def test_protocol_ambiguous_and_not_allowlisted():
    async def scenario():
        api = FakeAPI()
        async with Client(build_server(api)) as client:
            api.text = 'October 15; October 15'
            result = await client.call_tool('preview_document_update', dict(doc_id='doc1', tab_id='t.0', old_text='October 15', new_text='October 20'), raise_on_error=False)
            assert error_data(result)['error'] == 'AMBIGUOUS_MATCH'
            result = await client.call_tool('preview_document_update', dict(doc_id='another_doc', tab_id='t.0', old_text='x', new_text='y'), raise_on_error=False)
            assert error_data(result)['error'] == 'WRITE_NOT_ALLOWED'
            assert api.writes == 0
    run(scenario())


def test_stdio_subprocess_auth_required_without_browser(tmp_path):
    async def scenario():
        env = dict(os.environ, GOOGLE_ENV_FILE=str(tmp_path/'missing.env'), GOOGLE_TOKEN_PATH=str(tmp_path/'missing.json'),
                   GOOGLE_CLIENT_ID='', GOOGLE_CLIENT_SECRET='')
        transport = StdioTransport(command=sys.executable, args=[str(Path(__file__).with_name('server.py'))], env=env)
        async with Client(transport) as client:
            assert len(await client.list_tools()) == 4
            result = await client.call_tool('read_document', {'doc_id':'doc1'}, raise_on_error=False)
            assert result.is_error and error_data(result)['error'] == 'AUTH_REQUIRED'
            assert not list(tmp_path.iterdir())
    run(scenario())
