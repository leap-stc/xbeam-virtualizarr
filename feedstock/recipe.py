import xarray as xr
import apache_beam as beam
import xarray_beam as xbeam


# IO
reference_path = (
    "gs://leap-persistent/norlandrhagen/references/gridmet_1979_2020.parquet"
)
output_path = "gs://leap-scratch/norlandrhagen/outputs/gridmet_subset.zarr"

combined_ds = xr.open_dataset(reference_path, engine="kerchunk", chunks={})
# subset the reference zarr
source_dataset = combined_ds.isel(day=slice(0, 100))[["air_temperature"]]


source_chunks = dict(source_dataset.sizes)
target_chunks = {"day": 1, "lat": 585, "lon": 1386}
template = xbeam.make_template(source_dataset)
itemsize = max(variable.dtype.itemsize for variable in template.values())

with beam.Pipeline() as p:
    (
        p
        | xbeam.DatasetToChunks(source_dataset, source_chunks, split_vars=True)
        | xbeam.Rechunk(
            source_dataset.sizes, source_chunks, target_chunks, itemsize=itemsize
        )
        | xbeam.ChunksToZarr(output_path, template, target_chunks)
    )
