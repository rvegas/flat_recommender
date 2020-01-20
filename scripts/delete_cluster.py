from google.cloud import dataproc_v1 as dataproc


def delete_cluster():
    # Create a client with the endpoint set to the desired cluster region.
    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format('europe-west1')
    })

    # Create the cluster.
    operation = cluster_client.delete_cluster('big-data-architecture-ricardo', 'europe-west1', 'dataproc-bda')
    result = operation.result()

    # Output a success message.
    return 'Cluster deleted successfully'


def delete(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    return delete_cluster()
