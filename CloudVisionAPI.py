import io, os
import re
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format


def async_detect_document(gcs_source_uri, gcs_destination_uri):

    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
    client = vision.ImageAnnotatorClient()
    
    batch_size = 100
    mime_type = 'application/pdf'
    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    # gcs_source_uri = 'gs://filename'
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
    
    # gcs_destination_uri = 'gs://fileDestination '
    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)
    
    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config)
    
    operation = client.async_batch_annotate_files(requests=[async_request])
    operation.result(timeout=5000)
    
    storage_client = storage.Client()
    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    bucket = storage_client.get_bucket(bucket_name)
    
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    output = blob_list[0]
    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())
    
    response = json_format.Parse(
            json_string, vision.types.AnnotateFileResponse())
    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation
  
    print(u'Full text:')
    print(annotation.text)

files = 'file_name'
source_bucket = 'gs://cambridgefive_pdfs/'
destinations_bucket = 'gs://cambridgefive_pdfs/'
i = 0
while i < len(files):
#     async_detect_document(files[i], destinations[i])
    async_detect_document(source_bucket + files[i], source_bucket + files[i] + '.txt ')
    print(files[i])
    i+= 1
