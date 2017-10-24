# Transport For London GTFS Exporter

This simple Rust CLI allows you to fetch data from the
[Tfl Unified API][tfl-api] and transform it to [GTFS][gtfs].

[![Build Status](https://travis-ci.org/CommuteStream/tflgtfs.svg?branch=master)](https://travis-ci.org/CommuteStream/tflgtfs)
[![Clippy Linting Result](https://clippy.bashy.io/github/CommuteStream/tflgtfs/master/badge.svg)](https://clippy.bashy.io/github/CommuteStream/tflgtfs/master/log)


## Install

Clone [the repository][tfl-cli] and compile:

```sh
cargo build --release
```

## SSL issues

There have been SSL issues with the rust github repo resently. Workaround:

`ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt`

This is included in dockerfile and does not require action if building via Docker.


## Usage

Check the help `./target/release/tflgtfs help` for details.

In short, you can fetch Tfl lines with the `fetch-lines` command and transform
the cached values with the `transform gtfs` command.

You can do it in one shot via:

```sh
./target/release/tflgtfs fetch-lines --format gtfs
```

You will find the resulting GTFS files inside `./gtfs`.


## Development

When developing on nightly build it using the following command to actually
benefit from linting and Serde macro:

```
cargo build --features nightly --no-default-features
```


## License

See [License](./LICENSE).


[tfl-cli]: https://github.com/CommuteStream/tflgtfs/
[tfl-api]: https://api.tfl.gov.uk/
[gtfs]: https://developers.google.com/transit/gtfs/
[cargo-clippy]: https://crates.io/crates/cargo-clippy
