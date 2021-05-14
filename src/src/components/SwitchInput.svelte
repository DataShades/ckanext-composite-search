<script lang="ts">
  export let name: string
  export let value: boolean
  export let leftLabel: string
  export let rightLabel: string

  const toggle = () => value = !value;

</script>

<div class="switch-input" on:click={toggle} class:active={value}>
  <input {name} type="hidden" value={value || ''}/>
  <span class="switch-label">
    {leftLabel}
  </span>
  <span class="switch-wrapper">
    <span class="switch-handle"></span>
  </span>
  <span class="switch-label">
    {rightLabel}
  </span>

</div>

<style>
  .switch-input {
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  .switch-wrapper {
    position: relative;
    display: inline-block;
    background: #E6E6E6;
    width: 28px;
    height: 16px;
    border-radius: 30px;
    transition: background-color .3s;
    margin: 0 4px;
  }
  .active .switch-wrapper {
    background: #56BEA0;
  }
  .switch-handle {
    display: inline-block;
    margin: 2px;
    position: absolute;
    transition: all .3s;
    left: 0px;
    content: '';
    border-radius: 50%;
    width: 12px;
    height: 12px;
    background: #fff;
  }
  .active .switch-handle {
    left: 12px;
  }
</style>
