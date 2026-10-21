# R3-AF Goal Source Adapter

Uses the existing SphereRepository data as a **proof target source only**. It never generates GIVEN evidence. Literature-derived targets have priority. Unsupported generators remain unconverted. The adapter currently handles simple named stable generators and finite/free cyclic or direct-sum structures; it is not a complete parser for Toda generator expressions.

Run `run.ps1` from the project root. It backs up the goal selector and runs focused pytest only.
