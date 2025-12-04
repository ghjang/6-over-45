<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { Tab } from 's-comp-core';
	import LottoFrequency from './LottoFrequency.svelte';
	import NextGuess from './NextGuess.svelte';

	let tab: Tab;

	let tabs = [
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

	onMount(async () => {
		try {
			const response = await fetch(`${base}/data/latest_lottery_result.json`);
			const data = await response.json();
			const nextDrawNumber = parseInt(data.draw_number) + 1;

			tabs = [
				tabs[0],
				{
					...tabs[1],
					label: `${nextDrawNumber}회 당첨 번호 뽑기`
				}
			];
		} catch (e) {
			console.error('Failed to fetch lottery data:', e);
		}
	});
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
