# The official JGen blueprint catalog

JGen looks up short blueprint names here. With an entry for `terraform`, anyone can run:

```bash
jgen -g terraform -o tf.json            # latest version
jgen -g terraform@1.2.0 -o tf.json      # a specific version
jgen --search terraform                 # find it
```

The catalog is `catalog.json` on the default branch. JGen caches it for an hour.

## Adding a blueprint

1. Publish the blueprint in its own repository, either as a jar release or as a template-only repository with a
   version tag. See <https://jgen.chenile.org/remote-blueprints/>.
2. Open a pull request that adds an entry:

   ```json
   "terraform": {
     "source": "github:acme/jgen-terraform",
     "description": "A Terraform module with a CI workflow",
     "tags": ["terraform", "iac"],
     "versions": { "1.2.0": "<sha256 printed by jgen --fetch github:acme/jgen-terraform@1.2.0>" }
   }
   ```

   - `source` must be a `github:owner/repo` reference.
   - `versions` is optional. A pinned version's hash is enforced for everyone.
   - `blueprint` (optional) names the blueprint inside a jar that holds several.
3. The pull-request check validates the file.

**Listing here is an endorsement.** Sources in this catalog are trusted by JGen without asking, so review every
entry, and every change to one, as you would review code.

## Your own catalog

Any GitHub repository with a `catalog.json` in this format can serve as a catalog. Add it to
`~/.jgen/settings.json`:

```json
{
  "catalogs": [ { "source": "github:acme/jgen-catalog", "alias": "acme", "trusted": false } ]
}
```

Then `acme/terraform` picks that catalog's entry. Set `"trusted": true` only for a catalog you control.
