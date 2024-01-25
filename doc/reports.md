# Reports

## Tools and Technologies

Reports are generated using [evidence](evidence.dev). The source for the repo
are in `reports`. User reports done using a templated page with the parameter
used to select the correct user being the `uuid` field of the `UserAccount`
object of the data model. The `WebReport` object contains metadata specific to
each report.

Evidence uses a combination of SQL and JavaScript to build the report.


### Tips for working with Evidence

- Use `JSON.stringify(some_data)` to see the structure of a data object in the
  build report page
- JavaScript can be used to do some additional processing on the data e.g
  `heatmap_data.map(item => [item.name, item.value])`
- Move complex queries into separate SQL files but in general prefer to have
  data definitions adjacent to their use in charts or other components.
- Inputs do not work with custom ECharts components
- Search the [Evidence Slack](evidencedev.slack.com) or
  [Evidence GitHub repo](https://github.com/evidence-dev/evidence/issues/1465)
