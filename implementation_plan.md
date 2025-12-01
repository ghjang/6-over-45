# Implementation Plan - Lotto Ball UI

## Goal
Enhance the "Next Guess" tab UI by displaying lottery numbers as colored balls instead of plain text, as requested by the user.

## Proposed Changes

### [NEW] web/src/components/LottoBall.svelte
Create a new component to render a single lottery ball.
- **Props**: `number` (number)
- **Logic**: Determine background color based on number range.
    - 1-10: Yellow
    - 11-20: Blue
    - 21-30: Red
    - 31-40: Gray
    - 41-45: Green
- **Style**: Circular shape, centered text, shadow for 3D effect.

### [MODIFY] web/src/routes/NextGuess.svelte
- Import `LottoBall` component.
- Replace `guess.join(', ')` with an iteration rendering `LottoBall` for each number.
- Adjust CSS to align balls horizontally with spacing.

## Verification Plan

### Manual Verification
- Run `npm run preview` locally.
- Check if numbers are displayed as balls.
- Verify colors match the standard Lotto 6/45 colors.
