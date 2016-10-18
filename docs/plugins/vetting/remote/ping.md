The `ping` Vetting plugin is used to identify whether or not a server is pingable and populate Automatron's **facts** system with that information. This plugin is executed remotely and produces the following JSON output.

```json
{
    "ping": false
}
```

This data is used to populate the `facts['ping']` value.
