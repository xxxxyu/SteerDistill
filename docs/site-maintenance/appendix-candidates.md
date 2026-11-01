# Single-turn appendix candidates

The [candidate records](appendix-candidate-records.json) preserve three reviewed examples and their exact selected evidence for future article decisions. They use the same shared event/highlight schema as the published inline cases.

| Case | Capability illustrated | Current full-case code |
| --- | --- | --- |
| `java-node-interface` | Exact interface and tool-name selection | I1 |
| `export-sort-direction` | Sorting-direction parameter semantics | I3 |
| `recipe-science-tools` | Consecutive calls to correctly named tools | I2 |

The sorting example is the accepted article example. The other two remain candidates rather than additional article sections. All 21 method trajectories have one user turn; 28 selected actions were checked against raw records and 27 highlight spans were validated. This review did not alter the paper manuscript or the original trajectories.

Full cases resolve through `design-lab/paper-cases.html?group=inference&case=<slug>`. Resource references inside the JSON are site-relative and use the deployment prefix through `SitePaths.url()`.
