import os
import logging
import shutil

import docker
import legion
import legion.containers.docker
import legion.config
import legion.io
import legion.utils
import legion.test_utils.packaging

import legion_pyserve

LOGGER = logging.getLogger(__name__)


def get_wheel_with_actual_version(module):
    legion.test_utils.packaging.build_module_distribution(module)

    module_directory = legion.test_utils.packaging.find_directory_with_setup_py(module)
    return legion.test_utils.packaging.get_latest_distribution(module_directory)


def build(args, model_id, external_reader, client):
    model_file = args.model_file
    build_packages = args.build_packages_from_source
    python_package_version = args.python_package_version
    python_repository = args.python_repository
    docker_image_tag = args.docker_image_tag

    with legion.utils.TemporaryFolder('legion-docker-build') as temp_directory:
        folder, model_filename = os.path.split(model_file)

        shutil.copy2(model_file, os.path.join(temp_directory.path, model_filename))

        install_targets = 'legion', 'legion-toolchain-pyserve'
        wheel_target = False
        source_repository = ''

        if build_packages:
            install_targets = get_wheel_with_actual_version(legion), get_wheel_with_actual_version(legion_pyserve)
            wheel_target = True
            for target in install_targets:
                shutil.copy2(target, os.path.join(temp_directory.path, os.path.basename(target)))

            install_targets = [os.path.basename(path) for path in install_targets]
        else:
            if python_package_version:
                install_targets = ['{}=={}'.format(package, python_package_version) for package in install_targets]

            if python_repository:
                source_repository = '--extra-index-url %s' % python_repository

        # Copy additional payload from templates / docker_files
        additional_directory = os.path.join(
            os.path.dirname(__file__), 'templates', 'docker_files')

        for file in os.listdir(additional_directory):
            path = os.path.join(additional_directory, file)
            if os.path.isfile(path):
                shutil.copy2(path, os.path.join(temp_directory.path, file))

        base_image = args.base_docker_image
        if not base_image:
            base_image = 'legion/base-python-image:latest'

        data = {
            'DOCKER_BASE_IMAGE': base_image,
            'MODEL_ID': model_id,
            'MODEL_FILE': model_filename,
            'PIP_INSTALL_TARGETS': install_targets,
            'PIP_REPOSITORY': source_repository,
            'PIP_CUSTOM_TARGET': wheel_target
        }

        docker_file_content = legion.utils.render_template('Dockerfile.tmpl', data,
                                                           package_name=legion_pyserve.__name__)

        with open(os.path.join(temp_directory.path, 'Dockerfile'), 'w') as file:
            file.write(docker_file_content)

        labels = legion.containers.docker.generate_docker_labels_for_image(external_reader.path,
                                                                                 model_id,
                                                                                 args)
        labels = {k: str(v) if v else None for (k, v) in labels.items()}

        LOGGER.info('Building docker image in folder %s' % (temp_directory.path))
        try:
            image, _ = client.images.build(
                tag=docker_image_tag,
                nocache=True,
                path=temp_directory.path,
                rm=True,
                labels=labels
            )

        except docker.errors.BuildError as build_error:
            LOGGER.error('Cannot build image: %s' % (build_error))
            raise build_error

        LOGGER.info('Built image: %s', image)
        print('Built image: %s for model %s' % (image, model_id))

        return image




