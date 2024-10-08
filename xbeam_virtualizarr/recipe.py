import argparse


def run(argv=None, save_main_session=True):
    import xarray as xr
    import apache_beam as beam
    import xarray_beam as xbeam

    from apache_beam.options.pipeline_options import PipelineOptions
    from apache_beam.options.pipeline_options import SetupOptions

    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()

    _, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    # IO
    reference_path = (
        "gs://leap-persistent/norlandrhagen/references/gridmet_1979_2020.parquet"
    )
    # output_path = "gs://leap-scratch/norlandrhagen/outputs/gridmet_subset.zarr"
    # output_path = "gs://leap-scratch/norlandrhagen/outputs/gridmet_time_subset_all_vars.zarr"
    output_path = "gs://leap-scratch/norlandrhagen/outputs/gridmet_full.zarr"


    source_dataset = xr.open_dataset(reference_path, engine="kerchunk", chunks=None)
    # subset the reference zarr
    # source_dataset = combined_ds.isel(day=slice(0, 50000))[
    #     ["air_temperature"]
    # ]  # all vars
    # 1220 time steps, all vars. ie 200 time slices
    template = xbeam.make_template(source_dataset)
    # source_chunks = dict(source_dataset.sizes) # this is total size. Hardcode for now
    source_chunks = {"day": 61, "lat": 98, "lon": 231}
    target_chunks = {
        "day": 600,
        "lat": 98,
        "lon": 231,
    }  # bump chunks to 100MB. No major rechunking
    # target_chunks = {"day": 16, "lat": 585, "lon": 1386}  # ~ full map 100MB chunks

    itemsize = 8

    # ToDo: looks like template is needed! https://github.com/google/xarray-beam/issues/85

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | xbeam.DatasetToChunks(source_dataset, source_chunks, split_vars=True)
            | xbeam.Rechunk(
                source_dataset.sizes,
                source_chunks,
                target_chunks,
                itemsize=itemsize,
                max_mem=200000000.0,  # 200mb-ish
            )
            | xbeam.ChunksToZarr(store=output_path, template=template, zarr_chunks=target_chunks)
        )


if __name__ == "__main__":
    run()
