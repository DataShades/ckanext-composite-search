<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { FieldDetails } from "../utils";
    import type { FieldData } from "../types";

    import CloseCrossSvg from "./CloseCrossSvg.svelte";
    import NegationSwitch from "./NegationSwitch.svelte";
    import JunctionInput from "./JunctionInput.svelte";
    import TypeInput from "./TypeInput.svelte";
    import InputField from "./InputField.svelte";
    import SelectField from "./SelectField.svelte";
    import DotsSvg from "./DotsSvg.svelte";
    import CrossArrowSvg from "./CrossArrowSvg.svelte";

    const dispatch = createEventDispatcher();
    export let field: FieldData;
    export let isLast: boolean = false;

    $: definition = FieldDetails.definitions[field.type];
    const remove = () => dispatch("remove");
    const reset = () => {
        if (definition.type !== "text") {
            field.value = null;
        }
    };
</script>

<div class="composite-field">
    <div class="input">
        <i class="drag-handle left-drag-handle">
            <DotsSvg />
        </i>

        {#if definition.type === "text"}
            <InputField bind:field placeholder={definition.placeholder} />
        {:else if definition.type === "select"}
            <SelectField
                options={definition.options}
                bind:field
                placeholder={definition.placeholder}
            />
        {:else if definition.type === "autocomplete-select"}
            <SelectField
                options={definition.options}
                bind:field
                placeholder={definition.placeholder}
                autocomplete={true}
            />
        {:else}
            <strong>Unsupported field type</strong>
        {/if}
    </div>

    <i class="drag-handle center-drag-handle">
        <CrossArrowSvg />
    </i>
    <NegationSwitch bind:value={field.negation} />

    <div class="search-adjustment">
        <TypeInput on:change={reset} bind:value={field.type} />
        <JunctionInput disabled={isLast} bind:value={field.junction} />
    </div>

    <div class="remove-field-container">
        <button type="button" class="remove-field" on:click={remove} aria-label="Remove field">
            <CloseCrossSvg /></button
        >
    </div>
</div>

<style>
    .center-drag-handle {
        margin-inline-start: 8px;
    }
    .composite-field {
        border: 1px solid grey;
        border-radius: 5px;
        display: flex;
        align-items: center;
        line-height: 1rem;
        padding: 11px 24px;
        margin-bottom: 10px;
        background: #fff;
    }
    .input {
        flex: 1;
        width: 100%;

        display: flex;
        align-items: center;

        box-sizing: border-box;
    }

    .input .drag-handle {
        margin-inline-end: 8px;
    }
    .search-adjustment {
        display: flex;
        box-sizing: border-box;
    }

    .remove-field-container {
        width: fit-content;
    }

    .remove-field {
        background: none;
        border: none;
        padding: 0px;
        margin: 6px 0px;
        margin-inline-start: 24px;
        cursor: pointer;
    }

    @media (max-width: 992px) {
        .center-drag-handle {
            display: none;
        }

        .composite-field {
            flex-direction: column;
            row-gap: 16px;
            padding: 0;
        }

        .input {
            border-bottom: 1px solid #cccccc;
            padding: 16px;
        }
        .search-adjustment {
            gap: 16px;
            width: 100%;
            padding: 0 16px;
        }

        .remove-field-container {
            width: 100%;
            box-sizing: border-box;
            padding: 0 16px;
            margin-bottom: 16px;
        }
        .remove-field {
            background: #f4f4f4;
            border-radius: 4px;

            width: 100%;
            padding: 7px;
            margin: 0;
            box-sizing: border-box;
        }

        .remove-field:hover {
            background: #dcdcdc;
        }
    }

    @media (max-width: 450px) {
        .search-adjustment {
            flex-wrap: wrap;
        }
    }
</style>
