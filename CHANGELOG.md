# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for Kaifa KFM 95002630 T11252, firmware 1.03.
- Do not export stale data, by using a watchdog timer.
  This catches cases where the IR reader came detached or misaligned.
  Instead of stale data you will just have a gap in your graphs.

## [0.1.4] – 2022-04-04
## [0.1.3] – 2020-11-02
## [0.1.2] – 2020-11-02
## [0.1.1] – 2020-11-02
## [0.1.0] – 2020-11-02
