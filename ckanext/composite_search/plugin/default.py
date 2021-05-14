from typing import Dict, Any, List, Tuple

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckan.lib.search.query import solr_literal

from .base import ICompositeSearch, SearchParam


class DefaultSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(ICompositeSearch)

    # ICompositeSearch

    def before_composite_search(
        self, search_params: Dict[str, Any], params: List[SearchParam]
    ) -> Tuple[Dict[str, Any], List[SearchParam]]:
        query = ''
        for param in reversed(params):
            value = ' '.join([solr_literal(word) for word in param.value.split()])
            if not value:
                continue
            sign = '-' if tk.asbool(param.negation) else '+'
            fragment = f"{param.type}:* AND {sign}{param.type}:({value})"
            if query:
                query = f'{fragment} {param.junction} ({query})'
            else:
                query = fragment
        q = search_params.get('q', '')
        q += ' ' + query
        search_params['q'] = q
        return search_params, params
