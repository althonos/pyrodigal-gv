# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
[Unreleased]: https://github.com/althonos/pyrodigal-gv/compare/v0.3.1...HEAD


## [v0.3.1] - 2023-11-27
[v0.3.1]: https://github.com/althonos/pyrodigal-gv/compare/v0.3.0...v0.3.1

### Fixed
- Inconsistent behaviour introduced by 868bd18ad121ad59489f76da031c0cebc29ff53a ([apcamargo/genomad#56](https://github.com/apcamargo/genomad/issues/56)).


## [v0.3.0] - 2023-11-27
[v0.3.0]: https://github.com/althonos/pyrodigal-gv/compare/v0.2.0...v0.3.0

### Added
- Command line interface based off the `pyrodigal` CLI. 

### Fixed
- Avoid storing all-zero motif weights in `meta.json` file.

### Changed
- `pyrodigal` dependency version to `v3.2.1`.



## [v0.2.0] - 2023-10-24
[v0.2.0]: https://github.com/althonos/pyrodigal-gv/compare/v0.1.0...v0.2.0

### Added
- `min_mask` argument to `ViralGeneFinder` to control the minimum lenght of masked regions on `mask=True`.
- Explicit support for Python 3.12.

### Changed
- `pyrodigal` dependency version to `v3.1`.


## [v0.1.0] - 2023-09-17
[v0.1.0]: https://github.com/althonos/pyrodigal-gv/compare/13f7fb0...v0.1.0

Initial release.
