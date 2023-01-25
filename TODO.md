# TODO

## Documentation
 - Write high-level concuptual overview / introduction to architecture and concepts.
 - Tutorial showing how to use `simulation` package to create a basic simulation.

## Simulation package
 - Implement layered SimGraphs & "graphs of graphs" to represent simulation at varying levels of abstraction.
   - Support 'fallback' logic which comes into effect if a SimGraph update() call fails, to absorb the impulse in some other way. E.g. if a gear mesh locks up, maybe nothing happens, or maybe a motor driving the mesh burns out.
 - Support 'merging' non-circular causal paths.

## Misc
 - Move tests to own folder
    - Package simulation modules
 - Move pdoc into a github action so it runs on approved PR
 - SciFi Bounty Hunter Demo Game
    - TUI/GUI for playing the game instead of just testing it.
