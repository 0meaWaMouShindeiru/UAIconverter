

def print_errors(invalid_data):
    for error, annotation in invalid_data:
        print('-----------------')
        print('annotation_id: {}'.format(annotation['annotationId']))
        print('-----------------')
        print(error)
        print('-----------------')