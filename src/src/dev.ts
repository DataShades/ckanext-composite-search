import Example from "./Example.svelte";

const app = new Example({
    target: document.body,
    props: {
        enabled: true,
        prefix: "ext_composite_",
        order: [
            "any",
            "title",
            "description",
            "keyword",
            "topic",
            "purpose",
            "data_type",
            "attachment",
        ],
        definitions: {
            any: {
                type: "text",
                label: "Any attribute",
                placeholder: "Add a value",
                default: true,
            },
            title: { type: "text", label: "Title" },
            description: { type: "text", label: "Description" },
            keyword: { type: "text", label: "Keyword" },
            topic: { type: "text", label: "Topic" },
            purpose: { type: "text", label: "Purpose" },
            organization: {
                type: "autocomplete-select",
                label: "Organization",
                placeholder: "Choose organization",
                options: [
                    { label: "Mining Tenements (DMIRS-003)", value: "1" },
                    { label: "Heritage Areas (DPLH-089)", value: "2" },
                    { label: "Heritage List (DPLH-090)", value: "3" },
                    { label: "Public Transport Authority Rail Distance Measures (PTA-005)", value: "4" },
                    { label: "Distribution Overhead Powerlines (WP-031)", value: "5" },
                    { label: "Distribution Pole (WP-029)", value: "6" },
                    { label: "Distribution Underground Cables (WP-034)", value: "7" },
                    { label: "Electrical Enclosures (WP-040)", value: "8" },
                    { label: "Electrical Pillars (WP-041)", value: "9" },

                ],
            },
            format: {
                type: "autocomplete-select",
                label: "Format",
                placeholder: "Choose format",
                options: [
                    { label: "CSV", value: "csv" },
                    { label: "JPEG", value: "jpeg" },
                    { label: "XML", value: "xml" },
                    { label: "DRF", value: "drf" },
                    { label: "PPT", value: "ppt" },
                    { label: "PPTX", value: "pptx" },
                    { label: "GeoJSON", value: "geojson" },
                    { label: "JSON", value: "json" },
                    { label: "RAW", value: "raw" },
                ],
            },
            empty_or_not: {
                type: "autocomplete-select",
                label: "Empty or not",
                options: [
                    { label: "", value: "" },
                    { label: "Other", value: "other" },
                ],
            },
            empty_with_label: {
                type: "autocomplete-select",
                label: "Empty with label",
                options: [
                    { label: "hehe", value: "" },
                    { label: "Other", value: "other" },
                ],
            },

            attachment: { type: "text", label: "File Attachment or smth" },
        },
        data: [
            { type: "title", value: "dislike", junction: "OR", negation: true },
            { type: "organization", value: "9" },
            { type: "format", value: "" },
            { type: "empty_or_not", value: "" },
            { type: "empty_with_label", value: "" },
        ],
    },
});

export default app;
