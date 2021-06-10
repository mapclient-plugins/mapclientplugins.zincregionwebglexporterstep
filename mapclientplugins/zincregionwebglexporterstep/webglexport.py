from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.streamregion import StreaminformationRegion


def _read_region_description(region, region_description):
    stream_information = region.createStreaminformationRegion()
    memory_resource = stream_information.createStreamresourceMemoryBuffer(region_description['elements'])
    stream_information.setResourceDomainTypes(memory_resource, Field.DOMAIN_TYPE_MESH3D)

    for key in region_description:
        if key != 'elements':
            memory_resource = stream_information.createStreamresourceMemoryBuffer(region_description[key])
            stream_information.setResourceDomainTypes(memory_resource, Field.DOMAIN_TYPE_NODES)
            stream_information.setResourceAttributeReal(memory_resource, StreaminformationRegion.ATTRIBUTE_TIME,
                                                        key)
    region.read(stream_information)


def _read_scene_description(scene, scene_description):
    stream_information = scene.createStreaminformationScene()
    stream_information.setIOFormat(stream_information.IO_FORMAT_DESCRIPTION)
    stream_information.createStreamresourceMemoryBuffer(scene_description)
    scene.read(stream_information)


def export_to_web_gl_json(mesh_description):
    """
        Export graphics into JSON formats. Returns an array containing the
   string buffers for each export

    :param mesh_description:
    :return:
    """
    context = Context('web_gl')

    region_description = mesh_description.get_region_description()
    scene_description = mesh_description.get_scene_description()

    region = context.createRegion()
    scene = region.getScene()

    _read_region_description(region, region_description)
    _read_scene_description(scene, scene_description)

    start_time = mesh_description.get_start_time()
    end_time = mesh_description.get_end_time()
    epoch_count = mesh_description.get_epoch_count()

    stream_information = scene.createStreaminformationScene()
    stream_information.setIOFormat(stream_information.IO_FORMAT_THREEJS)
    stream_information.setInitialTime(start_time)
    stream_information.setFinishTime(end_time)
    stream_information.setNumberOfTimeSteps(epoch_count)
    stream_information.setOutputTimeDependentVertices(1)

    # Get the total number of graphics in a scene/region that can be exported
    number = stream_information.getNumberOfResourcesRequired()
    resources = []
    # Write out each graphics into a json file which can be rendered with our
    # WebGL script
    for i in range(number):
        resources.append(stream_information.createStreamresourceMemory())
    scene.write(stream_information)

    # Store all the resources in a buffer
    buffer = [resources[i].getBuffer()[1] for i in range(number)]

    return buffer
