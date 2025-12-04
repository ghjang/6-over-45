<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import LottoBall from '../components/LottoBall.svelte';

	let winningNumbers: number[] = [];
	let bonusNumber: number | null = null;
	let guesses: number[][] = [];
	let drawNumber: number | null = null;
	let loading = true;

	onMount(async () => {
		try {
			// Fetch latest result
			const resultResponse = await fetch(`${base}/data/latest_lottery_result.json`);
			const resultData = await resultResponse.json();

			drawNumber = parseInt(resultData.draw_number);
			winningNumbers = resultData.winning_numbers;
			bonusNumber = resultData.bonus_number;

			// Fetch guesses
			const guessesResponse = await fetch(`${base}/data/guesses.json`);
			const guessesData = await guessesResponse.json();

			// Find guesses for the current draw
			const drawKey = `draw_${drawNumber}`;
			const drawGuessesObj = guessesData.guesses.find((g: any) => g[drawKey]);

			if (drawGuessesObj) {
				guesses = drawGuessesObj[drawKey];
			}
		} catch (e) {
			console.error('Failed to load data:', e);
		} finally {
			loading = false;
		}
	});

	function isWinningNumber(num: number): boolean {
		return winningNumbers.includes(num);
	}

	function isBonusNumber(num: number): boolean {
		return num === bonusNumber;
	}

	function getRank(guess: number[]): string {
		const matchCount = guess.filter((n) => isWinningNumber(n)).length;
		const hasBonus = bonusNumber !== null && guess.includes(bonusNumber);

		if (matchCount === 6) return '1등';
		if (matchCount === 5 && hasBonus) return '2등';
		if (matchCount === 5) return '3등';
		if (matchCount === 4) return '4등';
		if (matchCount === 3) return '5등';
		return '';
	}
</script>

<div class="previous-result">
	{#if loading}
		<p>로딩 중...</p>
	{:else}
		<div class="section winning-section">
			<h3>{drawNumber}회 당첨 번호</h3>
			<div class="balls">
				{#each winningNumbers as num}
					<LottoBall number={num} />
				{/each}
				{#if bonusNumber}
					<div class="plus">+</div>
					<LottoBall number={bonusNumber} />
				{/if}
			</div>
		</div>

		<div class="section guesses-section">
			<h3>{drawNumber}회 예상 번호</h3>
			{#if guesses.length > 0}
				<ul>
					{#each guesses as guess}
						<li class="guess-row-container">
							<div class="guess-box">
								<div class="balls">
									{#each guess as num}
										<div
											class="ball-wrapper"
											class:match={isWinningNumber(num)}
											class:bonus={isBonusNumber(num)}
										>
											<LottoBall number={num} />
											{#if isWinningNumber(num) || isBonusNumber(num)}
												<div class="match-indicator"></div>
											{/if}
										</div>
									{/each}
								</div>
							</div>
							<div class="rank-text">
								{getRank(guess)}
							</div>
						</li>
					{/each}
				</ul>
			{:else}
				<p>해당 회차의 예상 번호가 없습니다.</p>
			{/if}
		</div>
	{/if}
</div>

<style lang="scss">
	.previous-result {
		padding: 1em;
		font-family: 'Noto Sans KR', sans-serif;

		.section {
			margin-bottom: 2em;

			h3 {
				margin-bottom: 1em;
				color: #333;
				border-left: 5px solid #ff9800;
				padding-left: 10px;
			}
		}

		.balls {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			gap: 0.5em;
		}

		.plus {
			font-size: 1.5em;
			font-weight: bold;
			color: #aaa;
			margin: 0 0.2em;
		}

		ul {
			list-style: none;
			padding: 0;
		}

		.guess-row-container {
			display: flex;
			align-items: center;
			margin-bottom: 0.8em;

			.guess-box {
				display: inline-flex;
				align-items: center;
				background: #f9f9f9;
				padding: 0.8em;
				border-radius: 8px;
				border: 1px solid #eee;
				width: max-content; /* Fit content */
				min-width: 350px; /* Ensure consistent minimum width */
				justify-content: center; /* Center balls if wider */
			}

			.rank-text {
				margin-left: 1em;
				font-weight: bold;
				color: #ff5722; /* Highlight rank text */
				font-size: 1.1em;
				min-width: 3em; /* Reserve space */
			}

			.ball-wrapper {
				position: relative;

				&.match {
					// Highlight effect for matching balls
					&::after {
						content: '';
						position: absolute;
						top: -5px;
						left: -5px;
						right: -5px;
						bottom: -5px;
						border: 2px solid #ff9800; /* Orange */
						border-radius: 50%;
						z-index: 0;
					}
				}

				&.bonus {
					// Different highlight for bonus ball
					&::after {
						content: '';
						position: absolute;
						top: -5px;
						left: -5px;
						right: -5px;
						bottom: -5px;
						border: 2px solid #2196f3; /* Blue for bonus */
						border-radius: 50%;
						z-index: 0;
					}
				}
			}
		}
	}
</style>
