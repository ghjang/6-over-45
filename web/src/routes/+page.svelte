<script lang="ts">
	import { Tab } from 's-comp-core';
	import LottoFrequency from './LottoFrequency.svelte';
	import NextGuess from './NextGuess.svelte';

	let tab: Tab;

	const tabs = [
		{
			label: '로또 당첨 번호 빈도',
			component: LottoFrequency,
			componentClassName: null
		},
		{
			label: '다음 당첨 번호 뽑기',
			component: NextGuess,
			componentClassName: null
		}
	];
</script>

<div class="tab-container">
	<Tab bind:this={tab} selectedTabIndex={1} {tabs} />
</div>

<style lang="scss">
	.tab-container {
		border: 1px solid darkgray;
		border-radius: 1px;
	}
</style>
