<script lang="ts">
  import CaretSvg from "./CaretSvg.svelte";
  import CloseCrossSvg from "./CloseCrossSvg.svelte";
  import { tick } from 'svelte';
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let name: string;
  export let value: any = null;
  export let placeholder: string = "";
  export let options: { label: string; value: any }[];

  let isOpen: boolean = false;
  let opts;
  let input;

  $: option = options.find(({ value: v }) => v === value);
  $: label = option ? option.label : label || "";

  function toggle() {
    isOpen = !isOpen;

    if (isOpen) {
      input.focus();
    }

    _selectFirst();
  }

  function close() {
    isOpen = false;
    document.activeElement.blur();
  }

  function open() {
    isOpen = true;
  }

  function onInput(e) {
    open();
    _unselectAll();
    _selectFirst();
  }

  function keyDispatcher(e) {
    let supportedKeys = [
      "ArrowDown",
      "ArrowUp",
      "Enter",
      "Backspace",
      "Escape",
    ];

    let selectedEl = opts.querySelector("li.selected");

    if (!supportedKeys.includes(e.key) || !opts) {
      if (selectedEl && e.key.length === 1) {
        // it's a symbol key, user is editing currently selected option
        value = "";
      }
      return;
    }

    if (e.key !== 'Backspace') {
      e.preventDefault();
    }



    switch (e.key) {
      case "Enter":
        if (!selectedEl) {
          return;
        }
        let itemValue = selectedEl.getAttribute("data-value");
        let itemLabel = selectedEl.getAttribute("data-label");

        select(itemLabel, itemValue);
        break;
      case "ArrowDown":
        open();

        if (hasClass(opts.querySelectorAll("li"), "selected")) {
          let nextEl = selectedEl.nextElementSibling;

          if (nextEl) {
            _unselectAll();
            nextEl.classList.add("selected");
            nextEl.scrollIntoView();
          }
        } else {
          _selectFirst();
        }
        break;
      case "ArrowUp":
        open();

        if (hasClass(opts.querySelectorAll("li"), "selected")) {
          let prevEl = selectedEl.previousElementSibling;

          if (prevEl) {
            _unselectAll();
            prevEl.classList.add("selected");
            prevEl.scrollIntoView();
          }
        } else {
          _selectFirst();
        }
        break;
      case "Backspace":
        value = "";
        break;
      case "Escape":
        close();
        break;
      default:
        break;
    }
  }

  async function select(l, v) {
    value = v;
    label = l;

    await tick();
    input.value = option ? option.label : "";

    dispatch("change", { value });
    close();
  }

  function search(l, v) {
    return l.toLowerCase().includes(v.toLowerCase());
  }

  function hasClass(arr, className) {
    for (let i = 0; i < arr.length; i++) {
      if (arr[i].classList.contains(className)) {
        return true;
      }
    }
    return false;
  }

  function _selectFirst() {
    if (opts && !_isSelected()) {
      let firstItem = opts.querySelector("li:first-child");
      if (firstItem) {
        firstItem.classList.add("selected");
      }
    }
  }

  function _isSelected() {
    return opts.querySelector("li.selected") ?? false;
  }

  function _unselectAll() {
    let selectedElements = opts.querySelectorAll("li.selected");
    for (let i = 0; i < selectedElements.length; i++) {
      selectedElements[i].classList.remove("selected");
    }
  }

  function highlight(label, searchText) {
    if (!searchText || searchText.length <= 1) {
      return label;
    }
    const regex = new RegExp(RegExp.escape(searchText), "gi");
    return label.replace(regex, '<mark class="highlight">$&</mark>');
  }

  function clear() {
    value = "";
    label = "";
    close();
  }

  function optionClick() {
    this.classList.add('selected');
    select(
      this.getAttribute('data-label'),
      this.getAttribute('data-value')
    );

  }
</script>

<div class="select2" class:active={isOpen}>
  <input type="hidden" {name} {value} />
  <div class="select2_selected" on:click={toggle}>
    <span class="select2_selected--label">
      <input
        bind:this={input}
        bind:value={label}
        {placeholder}
        on:keydown={keyDispatcher}
        on:input={onInput}
        autocomplete="off"
      />
    </span>
    {#if label}
      <i class="cross-icon" on:click|stopPropagation={clear}>
        <CloseCrossSvg />
      </i>
    {/if}
    <i class="caret-icon">
      <CaretSvg />
    </i>
  </div>

  <ul
    class="select2_options"
    class:show={isOpen}
    data-simplebar
    bind:this={opts}
    on:mouseleave="{close}"
  >
    {#each options as opt (opt.value)}
      {#if search(opt.label, label)}
        <li
          class="select2-options--option"
          class:selected={value === opt.value}
          data-value={opt.value}
          data-label={opt.label}
          role="option"
          on:click={() => {select(opt.label, opt.value)}}
        >
          {@html highlight(opt.label, label)}
        </li>
      {/if}
    {/each}
  </ul>
</div>

<style>
  .select2 {
    position: relative;
  }
  .select2_selected {
    display: flex;
    align-items: center;

    padding: 5px 5px 5px 0;
  }
  .select2_selected .caret-icon,
  .select2_selected .cross-icon {
    cursor: pointer;
  }
  .select2_selected .cross-icon {
    margin-right: 10px;
  }
  .select2_selected--label {
    width: 100%;
  }
  .select2_selected--label input {
    width: 100%;
    border: none;
    outline: none;
  }
  .select2_options {
    position: absolute;
    display: none;
    margin: 0px;
    padding: 0;
    margin-inline-start: -2px;
    width: 100%;
    z-index: 1;
    list-style: none;
    background: #fff;
    border: 2px solid #e6e6e6;
    max-height: 200px;
    overflow-y: auto;
    font-size: 14px;
  }
  .select2_options:empty {
    padding: 10px;
  }
  .select2_options:empty:after {
    content: "No results found";
    margin-top: 10px;
  }
  .select2_options.show {
    display: block;
  }
  .select2-options--option {
    padding: 4px 10px;
    margin: 4px;

    cursor: pointer;
  }
  .select2-options--option:hover {
    background-color: #f1f1f1;
  }
  .select2-options--option.selected {
    background-color: #dcdcdc;
  }

  @media (max-width: 480px) {
    .select2 {
        width: 100%;
    }
  }
</style>
