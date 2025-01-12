# CHANGELOG


## v0.7.2 (2025-01-12)

### Bug Fixes

- Extend reboot wait time to 15 seconds
  ([`2775c39`](https://github.com/gtaylor/baymesh-cli/commit/2775c3994a23133b356f6b60e9f83beae087c2d0))

Turns out that the G2 is even slower than the T-Beam.

- Silence serial logger during setup
  ([`bda9580`](https://github.com/gtaylor/baymesh-cli/commit/bda9580dbcfd2d123b0fae40cefd07c36bbdae1c))

- Typo
  ([`2837db5`](https://github.com/gtaylor/baymesh-cli/commit/2837db5b84919b1669376d8c431ebe2e3e118796))

### Chores

- Bump version in uv.lock
  ([`09e4e80`](https://github.com/gtaylor/baymesh-cli/commit/09e4e8064be0b3dc6ee18f96fb3b699c10f7f572))


## v0.7.1 (2025-01-12)

### Bug Fixes

- Fall back to sleeping through reboots
  ([`0bb5b55`](https://github.com/gtaylor/baymesh-cli/commit/0bb5b559bccca0c1e3b6f79990584b27c59b6bd8))

I had originally tried to find a way to wait for nodes to reboot when applying settings to keep
  things fast and dynamic, but I couldn't find a safe way to detect when the node was back up 100%
  of the time on all of the devices I had.

Fall back to a plain old sleep and let's hope that most devices reboot within 10 seconds.

- Remove unused imports
  ([`966e337`](https://github.com/gtaylor/baymesh-cli/commit/966e3373b60d567cdb99fa76f19673b92d186221))

### Chores

- Bump version in uv.lock
  ([`f71b607`](https://github.com/gtaylor/baymesh-cli/commit/f71b607070010c4a031dafb58159a4e693c8e553))


## v0.7.0 (2025-01-11)

### Bug Fixes

- Correct info emit colors
  ([`5f940e3`](https://github.com/gtaylor/baymesh-cli/commit/5f940e3ff7626557d7795aa836775f178c377185))

Was previously cyan but was supposed to be color-less.

### Chores

- Upgrade dependencies
  ([`efdb242`](https://github.com/gtaylor/baymesh-cli/commit/efdb242fadcf768a9ce5f56b826bb62cbb89d565))

### Code Style

- Remove some padding in node_validation
  ([`34ecf8e`](https://github.com/gtaylor/baymesh-cli/commit/34ecf8eecc0c6c078194129e93b8b015f9235009))

### Documentation

- Fix brew install path in README
  ([`9dc42cf`](https://github.com/gtaylor/baymesh-cli/commit/9dc42cf3f5e6c45c7f6dad5516c36b10dd664f19))

- Update README.md usage instructions
  ([`8c225f4`](https://github.com/gtaylor/baymesh-cli/commit/8c225f4ed9609f0f0c26a8166ddbed6b11e7a9d0))

### Features

- Show long/short name when starting setup
  ([`59db496`](https://github.com/gtaylor/baymesh-cli/commit/59db496d170e5ee333a5a3163d9deec6eea40fd2))

This will make it more clear which node you are interacting with.


## v0.6.0 (2025-01-10)

### Bug Fixes

- Version comparison
  ([`3ac7596`](https://github.com/gtaylor/baymesh-cli/commit/3ac759662e4df0c2d4619cc09498706d2d188ada))

### Chores

- Bump dependencies
  ([`53be031`](https://github.com/gtaylor/baymesh-cli/commit/53be031a85cb04ca5e1781682786eca6d903607e))

- Commit the updated uv.lock version
  ([`b7cb817`](https://github.com/gtaylor/baymesh-cli/commit/b7cb817de09cb1e7262bc4cfd4c19f4109c3d28e))

- Remove Homebrew release stuff from CI
  ([`4f81bb5`](https://github.com/gtaylor/baymesh-cli/commit/4f81bb57c52d1192bde05cc9970cea9bd0747df3))

### Features

- Add node setup wizard
  ([`c5d8e39`](https://github.com/gtaylor/baymesh-cli/commit/c5d8e39633c8241349b2fa33fc8d19e3fff6a412))

The wizard will walk the user through configuring the essential settings for the node. For ex: LoRa
  preset, long/short names, etc.

- Add version checking
  ([`31bc074`](https://github.com/gtaylor/baymesh-cli/commit/31bc0740c299840c94f3242e9253ca758ae18e5d))

Since the recommended configs may change over time, it's important that users stay up to date. This
  commit adds a facility for checking for updates and notifying the user if a newer version is
  available.

For now we're checking on every command invocation, but we can cache this in the future if it
  becomes problematic.


## v0.5.1 (2025-01-07)

### Bug Fixes

- Pull Homebrew bump into ci.yml
  ([`a1d6bb8`](https://github.com/gtaylor/baymesh-cli/commit/a1d6bb8681e05829d751249b93dd000b0f29ac31))


## v0.5.0 (2025-01-07)

### Features

- Unveil the new Homebrew tap
  ([`4032861`](https://github.com/gtaylor/baymesh-cli/commit/4032861a3691102c04261c88572db1ace8a64aa0))


## v0.4.0 (2025-01-07)

### Documentation

- Remove testing changelog entries
  ([`73196b6`](https://github.com/gtaylor/baymesh-cli/commit/73196b686997f08f343fc20e5d50f6c0a6462085))

### Features

- Automate the release to baymesh Homebrew tap
  ([`b90fff0`](https://github.com/gtaylor/baymesh-cli/commit/b90fff04aa0198303d4197147177d708b5acfde6))


## v0.3.3 (2025-01-05)

### Bug Fixes

- Fix release for real this time
  ([`caaa9c9`](https://github.com/gtaylor/baymesh-cli/commit/caaa9c961570089a77f528889db14ce9cfdd1538))


## v0.3.2 (2025-01-05)

### Bug Fixes

- Fix release for real this time
  ([`eab6a5b`](https://github.com/gtaylor/baymesh-cli/commit/eab6a5b9d9de74bc0afec7bc84116f6101881ef9))


## v0.3.1 (2025-01-05)

### Bug Fixes

- Remove now-unused release.yml
  ([`7ed0adc`](https://github.com/gtaylor/baymesh-cli/commit/7ed0adca911258a5693af43e57eab24f73395276))


## v0.3.0 (2025-01-05)

### Features

- Attempt release automation fix
  ([`2ead208`](https://github.com/gtaylor/baymesh-cli/commit/2ead2082f217634a73445463f5fd918032370a32))


## v0.2.0 (2025-01-05)

### Features

- Attempt release automation fix
  ([`bb18bf7`](https://github.com/gtaylor/baymesh-cli/commit/bb18bf73cdadee6f3f83273460b772d950a6f2a5))


## v0.1.0 (2025-01-05)

### Documentation

- Add dev setup to README.md
  ([`3b72ec4`](https://github.com/gtaylor/baymesh-cli/commit/3b72ec4284b901d50b216ef75ac047283e72ebd3))

### Features

- Graduating to alpha
  ([`5015cfc`](https://github.com/gtaylor/baymesh-cli/commit/5015cfcf65d473e4a52a4173f475a6aa797b2649))


## v0.0.0 (2025-01-05)
