from __future__ import annotations
import logging
from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ..utils import SearchParam
from ..interfaces import ICompositeSearch

log = logging.getLogger(__name__)

CONFIG_PREFIX = "ckanext.composite_search.prefix"
DEFAULT_PREFIX = "ext_composite_"


def get_prefix() -> str:
    return toolkit.config.get(CONFIG_PREFIX, DEFAULT_PREFIX)


class CompositeSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_resource("../assets", "composite_search")

    # ITemplateHelpers
    def get_helpers(self):
        return {"composite_search_get_prefix": get_prefix}

    # IPackageController

    def before_search(self, search_params: dict[str, Any]) -> dict[str, Any]:
        prefix = get_prefix()
        original_extras = search_params.get("extras", {})
        if not any(prefix + key in original_extras for key in SearchParam.keys):
            # It's internal call via `get_action`
            return search_params

        try:
            # cannot use search_params["extras"] because they don't contain
            # values from empty/unchecked fields
            extras = [toolkit.request.args.getlist(prefix + k) for k in SearchParam.keys]
        except KeyError as e:
            log.debug('Missing key: %s', e)
            return search_params

        params = [
            SearchParam(*record)
            for record in zip(*extras)
            if record[0]
        ]

        for plugin in plugins.PluginImplementations(ICompositeSearch):
            search_params, params = plugin.before_composite_search(
                search_params, params
            )
        return search_params

    before_dataset_search = before_search
