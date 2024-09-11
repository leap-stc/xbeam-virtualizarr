import xarray as xr
import apache_beam as beam
import xarray_beam as xbeam
import argparse

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

def run(argv=None, save_main_session=True):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()


    _, pipeline_args = parser.parse_known_args(argv)


    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session


    with beam.Pipeline(options=pipeline_options) as p:
        (p
        | beam.Map(p))
    #     # IO
    #     reference_path = (
    #         "gs://leap-persistent/norlandrhagen/references/gridmet_1979_2020.parquet"
    #     )
    #     output_path = "gs://leap-scratch/norlandrhagen/outputs/gridmet_subset.zarr"

    #     combined_ds = xr.open_dataset(reference_path, engine="kerchunk", chunks={})
    #     # subset the reference zarr
    #     source_dataset = combined_ds.isel(day=slice(0, 1000))[
    #         ["air_temperature"]
    #     ]  # ~ 6.5 gb

    #     source_chunks = dict(source_dataset.sizes)
    #     target_chunks = {"day": 16, "lat": 585, "lon": 1386}  # ~ full map 100MB chunks
    #     template = xbeam.make_template(source_dataset)
    #     itemsize = max(variable.dtype.itemsize for variable in template.values())

    #     with beam.Pipeline(options=pipeline_options) as p:
    #         (
    #             p
    #             | xbeam.DatasetToChunks(source_dataset, source_chunks, split_vars=True)
    #             | xbeam.Rechunk(
    #                 source_dataset.sizes,
    #                 source_chunks,
    #                 target_chunks,
    #                 itemsize=itemsize,
    #             )
    #             | xbeam.ChunksToZarr(output_path, template, target_chunks)
    #         )


if __name__ == "__main__":
    run()
