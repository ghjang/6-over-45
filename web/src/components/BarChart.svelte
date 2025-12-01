<script lang="ts">
	import { barChart } from '../actions/barChart';
	import type { ChartOptions } from './chartTypes';

	export let chartOptions: ChartOptions;
	export let maxWidth: string = '800px';
</script>

<div class="chart-container" style:max-width={maxWidth}>
	<svg use:barChart={chartOptions}></svg>
</div>

<style lang="scss">
	.chart-container {
		width: 100%;
		overflow-x: auto;

		svg {
			display: block;
			margin: 0 auto;
		}
	}
</style>
