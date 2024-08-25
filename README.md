## Crossword Puzzle Game built with Cursor AI help

Cursor AI (with Claude 3.5 Sonnet) contributions:
- Generated the initial Python CLI version (prompt: "implement a simple cli-based crossword game").
- It got the game mechanics right.
- It created a simple stub for crossword generation: grid and used words structures, random word placement with multiple attempts and two directions, checking for intersections when placing words. It generated sample list of words and clues.
- It generated a simple web interface (prompt: "could you please create a simple web interface to play this game?") and made a couple of iterations on it with simple prompts ("add a button to check answers", "highlight incorrect words with red", "add possibility of navigation in crossword with arrows").

My contributions:
- Made the crossword generation more interesting: place words only with intersections, based on positions of already placed words instead of random placement on the grid. Make sure there's space between words on the grid and it's readable.
- Fix game mechanics: hide unsolved words and include clue numbers in the grid.

Observations:
- Initial AI-generated versions of both CLI game and web interface were surprisingly good.
- I wasn't successful in making significant changes to the crossword generation algorithm via prompting. However, I was able to make small incremental changes with prompting while iterating on the algorithm myself.
- Changing web UI with prompting worked much better, I didn't write any code myself.
- Semantic refactorings (such as "replace all prints of (x, y) with this method call; where (x, y) are different values in each callsite") and data generation (words and clues) were quite useful too.
- Code generation is very fast, in 95% of cases I felt the workflow was quite natural and seamless.