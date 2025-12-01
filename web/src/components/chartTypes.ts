export type ChartType = 'bar_chart' | 'line_chart';

export interface ChartOptions {
	type: ChartType;
	data: number[];
	dataWithoutBonus?: number[];
	dataWithBonus?: number[];
	width: number;
	height: number;
	margin: { top: number; right: number; bottom: number; left: number };
	barColorDefault: string;
	barColorHover: string;
	barColorSameValue: string;
	stripeColor: string;
	highlightColorMin: string;
	highlightColorMax: string;
	highlightColorMid: string;
	textColorFrequency: string;
	guideLineColor: string;
	transitionDuration: number;
	barBorderColor: string;
}
