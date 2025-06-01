<script lang="ts">
  import {prefix} from '../stores';
  import SwitchInput from './SwitchInput.svelte'
  export let value: boolean = false;

</script>


<SwitchInput bind:value name="{$prefix}negation" leftLabel="Is" rightLabel="Not" />
