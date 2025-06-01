from __future__ import annotations
from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckan.lib.search.query import solr_literal

from ..interfaces import ICompositeSearch
from ..utils import SearchParam

CONFIG_LITERAL_QUOTES = "ckanext.composite_search.plugin.default.literal_quotes"
DEFAULT_LITERAL_QUOTES = "double"

CONFIG_KEYWORDS = "ckanext.composite_search.plugin.default.keyword_fields"
DEFAULT_KEYWORDS = []


def single_quote_solr_literal(t: str) -> str:
    escaped = t.replace("'", r"\'")
    return f"'{escaped}'"


def both_quote_solr_literal(t: str) -> str:
    single = single_quote_solr_literal(t)
    double = solr_literal(t)
    return f"{single} OR {double}"

_literals = {
    "single": single_quote_solr_literal,
    "double": solr_literal,
    "both": both_quote_solr_literal,

}


class DefaultSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(ICompositeSearch)

    # ICompositeSearch

    def before_composite_search(
        self, search_params: dict[str, Any], params: list[SearchParam]
    ) -> tuple[dict[str, Any], list[SearchParam]]:
        query = ''

        for param in reversed(params):
            value = self._cs_prepare_value(param)
            if not value:
                continue

            if tk.asbool(param.negation):
                fragment = f"({param.type}:* AND -{param.type}:({value}))"

            else:
                fragment = f"{param.type}:({value})"

            if query:
                query = f'{fragment} {param.junction.upper()} ({query})'
            else:
                query = fragment

        q = search_params.get('q', '')
        q += ' ' + query
        search_params['q'] = q.strip()

        return search_params, params

    def _cs_prepare_value(self, param: SearchParam):
        """Escape search term.

        Split term string into separate tokens(words) before escaping.
        In case of keyword-field, just escape the value, without splitting.
        """
        literal = _literals[tk.config.get(CONFIG_LITERAL_QUOTES, DEFAULT_LITERAL_QUOTES)]
        keywords = set(tk.aslist(tk.config.get(CONFIG_KEYWORDS, DEFAULT_KEYWORDS)))

        if param.type in keywords:
            return literal(param.value)

        return ' '.join(literal(word) for word in param.value.split())
