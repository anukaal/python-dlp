# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import gapic_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.dlp_v2.types import dlp
from google.protobuf import empty_pb2  # type: ignore
from .base import DlpServiceTransport, DEFAULT_CLIENT_INFO


class DlpServiceGrpcTransport(DlpServiceTransport):
    """gRPC backend transport for DlpService.

    The Cloud Data Loss Prevention (DLP) API is a service that
    allows clients to detect the presence of Personally Identifiable
    Information (PII) and other privacy-sensitive data in user-
    supplied, unstructured data streams, like text blocks or images.
    The service also includes methods for sensitive data redaction
    and scheduling of data scans on Google Cloud Platform based data
    sets.
    To learn more about concepts and find how-to guides see
    https://cloud.google.com/dlp/docs/.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "dlp.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "dlp.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def inspect_content(
        self,
    ) -> Callable[[dlp.InspectContentRequest], dlp.InspectContentResponse]:
        r"""Return a callable for the inspect content method over gRPC.

        Finds potentially sensitive info in content.
        This method has limits on input size, processing time,
        and output size.
        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.
        For how to guides, see
        https://cloud.google.com/dlp/docs/inspecting-images and
        https://cloud.google.com/dlp/docs/inspecting-text,

        Returns:
            Callable[[~.InspectContentRequest],
                    ~.InspectContentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "inspect_content" not in self._stubs:
            self._stubs["inspect_content"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/InspectContent",
                request_serializer=dlp.InspectContentRequest.serialize,
                response_deserializer=dlp.InspectContentResponse.deserialize,
            )
        return self._stubs["inspect_content"]

    @property
    def redact_image(
        self,
    ) -> Callable[[dlp.RedactImageRequest], dlp.RedactImageResponse]:
        r"""Return a callable for the redact image method over gRPC.

        Redacts potentially sensitive info from an image.
        This method has limits on input size, processing time,
        and output size. See
        https://cloud.google.com/dlp/docs/redacting-sensitive-
        data-images to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        Returns:
            Callable[[~.RedactImageRequest],
                    ~.RedactImageResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "redact_image" not in self._stubs:
            self._stubs["redact_image"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/RedactImage",
                request_serializer=dlp.RedactImageRequest.serialize,
                response_deserializer=dlp.RedactImageResponse.deserialize,
            )
        return self._stubs["redact_image"]

    @property
    def deidentify_content(
        self,
    ) -> Callable[[dlp.DeidentifyContentRequest], dlp.DeidentifyContentResponse]:
        r"""Return a callable for the deidentify content method over gRPC.

        De-identifies potentially sensitive info from a
        ContentItem. This method has limits on input size and
        output size. See
        https://cloud.google.com/dlp/docs/deidentify-sensitive-
        data to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        Returns:
            Callable[[~.DeidentifyContentRequest],
                    ~.DeidentifyContentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "deidentify_content" not in self._stubs:
            self._stubs["deidentify_content"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/DeidentifyContent",
                request_serializer=dlp.DeidentifyContentRequest.serialize,
                response_deserializer=dlp.DeidentifyContentResponse.deserialize,
            )
        return self._stubs["deidentify_content"]

    @property
    def reidentify_content(
        self,
    ) -> Callable[[dlp.ReidentifyContentRequest], dlp.ReidentifyContentResponse]:
        r"""Return a callable for the reidentify content method over gRPC.

        Re-identifies content that has been de-identified. See
        https://cloud.google.com/dlp/docs/pseudonymization#re-identification_in_free_text_code_example
        to learn more.

        Returns:
            Callable[[~.ReidentifyContentRequest],
                    ~.ReidentifyContentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reidentify_content" not in self._stubs:
            self._stubs["reidentify_content"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ReidentifyContent",
                request_serializer=dlp.ReidentifyContentRequest.serialize,
                response_deserializer=dlp.ReidentifyContentResponse.deserialize,
            )
        return self._stubs["reidentify_content"]

    @property
    def list_info_types(
        self,
    ) -> Callable[[dlp.ListInfoTypesRequest], dlp.ListInfoTypesResponse]:
        r"""Return a callable for the list info types method over gRPC.

        Returns a list of the sensitive information types
        that the DLP API supports. See
        https://cloud.google.com/dlp/docs/infotypes-reference to
        learn more.

        Returns:
            Callable[[~.ListInfoTypesRequest],
                    ~.ListInfoTypesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_info_types" not in self._stubs:
            self._stubs["list_info_types"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ListInfoTypes",
                request_serializer=dlp.ListInfoTypesRequest.serialize,
                response_deserializer=dlp.ListInfoTypesResponse.deserialize,
            )
        return self._stubs["list_info_types"]

    @property
    def create_inspect_template(
        self,
    ) -> Callable[[dlp.CreateInspectTemplateRequest], dlp.InspectTemplate]:
        r"""Return a callable for the create inspect template method over gRPC.

        Creates an InspectTemplate for re-using frequently
        used configuration for inspecting content, images, and
        storage. See https://cloud.google.com/dlp/docs/creating-
        templates to learn more.

        Returns:
            Callable[[~.CreateInspectTemplateRequest],
                    ~.InspectTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_inspect_template" not in self._stubs:
            self._stubs["create_inspect_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/CreateInspectTemplate",
                request_serializer=dlp.CreateInspectTemplateRequest.serialize,
                response_deserializer=dlp.InspectTemplate.deserialize,
            )
        return self._stubs["create_inspect_template"]

    @property
    def update_inspect_template(
        self,
    ) -> Callable[[dlp.UpdateInspectTemplateRequest], dlp.InspectTemplate]:
        r"""Return a callable for the update inspect template method over gRPC.

        Updates the InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Returns:
            Callable[[~.UpdateInspectTemplateRequest],
                    ~.InspectTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_inspect_template" not in self._stubs:
            self._stubs["update_inspect_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/UpdateInspectTemplate",
                request_serializer=dlp.UpdateInspectTemplateRequest.serialize,
                response_deserializer=dlp.InspectTemplate.deserialize,
            )
        return self._stubs["update_inspect_template"]

    @property
    def get_inspect_template(
        self,
    ) -> Callable[[dlp.GetInspectTemplateRequest], dlp.InspectTemplate]:
        r"""Return a callable for the get inspect template method over gRPC.

        Gets an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Returns:
            Callable[[~.GetInspectTemplateRequest],
                    ~.InspectTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_inspect_template" not in self._stubs:
            self._stubs["get_inspect_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/GetInspectTemplate",
                request_serializer=dlp.GetInspectTemplateRequest.serialize,
                response_deserializer=dlp.InspectTemplate.deserialize,
            )
        return self._stubs["get_inspect_template"]

    @property
    def list_inspect_templates(
        self,
    ) -> Callable[[dlp.ListInspectTemplatesRequest], dlp.ListInspectTemplatesResponse]:
        r"""Return a callable for the list inspect templates method over gRPC.

        Lists InspectTemplates.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Returns:
            Callable[[~.ListInspectTemplatesRequest],
                    ~.ListInspectTemplatesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_inspect_templates" not in self._stubs:
            self._stubs["list_inspect_templates"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ListInspectTemplates",
                request_serializer=dlp.ListInspectTemplatesRequest.serialize,
                response_deserializer=dlp.ListInspectTemplatesResponse.deserialize,
            )
        return self._stubs["list_inspect_templates"]

    @property
    def delete_inspect_template(
        self,
    ) -> Callable[[dlp.DeleteInspectTemplateRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete inspect template method over gRPC.

        Deletes an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Returns:
            Callable[[~.DeleteInspectTemplateRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_inspect_template" not in self._stubs:
            self._stubs["delete_inspect_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/DeleteInspectTemplate",
                request_serializer=dlp.DeleteInspectTemplateRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_inspect_template"]

    @property
    def create_deidentify_template(
        self,
    ) -> Callable[[dlp.CreateDeidentifyTemplateRequest], dlp.DeidentifyTemplate]:
        r"""Return a callable for the create deidentify template method over gRPC.

        Creates a DeidentifyTemplate for re-using frequently
        used configuration for de-identifying content, images,
        and storage. See
        https://cloud.google.com/dlp/docs/creating-templates-
        deid to learn more.

        Returns:
            Callable[[~.CreateDeidentifyTemplateRequest],
                    ~.DeidentifyTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_deidentify_template" not in self._stubs:
            self._stubs["create_deidentify_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/CreateDeidentifyTemplate",
                request_serializer=dlp.CreateDeidentifyTemplateRequest.serialize,
                response_deserializer=dlp.DeidentifyTemplate.deserialize,
            )
        return self._stubs["create_deidentify_template"]

    @property
    def update_deidentify_template(
        self,
    ) -> Callable[[dlp.UpdateDeidentifyTemplateRequest], dlp.DeidentifyTemplate]:
        r"""Return a callable for the update deidentify template method over gRPC.

        Updates the DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Returns:
            Callable[[~.UpdateDeidentifyTemplateRequest],
                    ~.DeidentifyTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_deidentify_template" not in self._stubs:
            self._stubs["update_deidentify_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/UpdateDeidentifyTemplate",
                request_serializer=dlp.UpdateDeidentifyTemplateRequest.serialize,
                response_deserializer=dlp.DeidentifyTemplate.deserialize,
            )
        return self._stubs["update_deidentify_template"]

    @property
    def get_deidentify_template(
        self,
    ) -> Callable[[dlp.GetDeidentifyTemplateRequest], dlp.DeidentifyTemplate]:
        r"""Return a callable for the get deidentify template method over gRPC.

        Gets a DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Returns:
            Callable[[~.GetDeidentifyTemplateRequest],
                    ~.DeidentifyTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_deidentify_template" not in self._stubs:
            self._stubs["get_deidentify_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/GetDeidentifyTemplate",
                request_serializer=dlp.GetDeidentifyTemplateRequest.serialize,
                response_deserializer=dlp.DeidentifyTemplate.deserialize,
            )
        return self._stubs["get_deidentify_template"]

    @property
    def list_deidentify_templates(
        self,
    ) -> Callable[
        [dlp.ListDeidentifyTemplatesRequest], dlp.ListDeidentifyTemplatesResponse
    ]:
        r"""Return a callable for the list deidentify templates method over gRPC.

        Lists DeidentifyTemplates.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Returns:
            Callable[[~.ListDeidentifyTemplatesRequest],
                    ~.ListDeidentifyTemplatesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_deidentify_templates" not in self._stubs:
            self._stubs["list_deidentify_templates"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ListDeidentifyTemplates",
                request_serializer=dlp.ListDeidentifyTemplatesRequest.serialize,
                response_deserializer=dlp.ListDeidentifyTemplatesResponse.deserialize,
            )
        return self._stubs["list_deidentify_templates"]

    @property
    def delete_deidentify_template(
        self,
    ) -> Callable[[dlp.DeleteDeidentifyTemplateRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete deidentify template method over gRPC.

        Deletes a DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Returns:
            Callable[[~.DeleteDeidentifyTemplateRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_deidentify_template" not in self._stubs:
            self._stubs["delete_deidentify_template"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/DeleteDeidentifyTemplate",
                request_serializer=dlp.DeleteDeidentifyTemplateRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_deidentify_template"]

    @property
    def create_job_trigger(
        self,
    ) -> Callable[[dlp.CreateJobTriggerRequest], dlp.JobTrigger]:
        r"""Return a callable for the create job trigger method over gRPC.

        Creates a job trigger to run DLP actions such as
        scanning storage for sensitive information on a set
        schedule. See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        Returns:
            Callable[[~.CreateJobTriggerRequest],
                    ~.JobTrigger]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_job_trigger" not in self._stubs:
            self._stubs["create_job_trigger"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/CreateJobTrigger",
                request_serializer=dlp.CreateJobTriggerRequest.serialize,
                response_deserializer=dlp.JobTrigger.deserialize,
            )
        return self._stubs["create_job_trigger"]

    @property
    def update_job_trigger(
        self,
    ) -> Callable[[dlp.UpdateJobTriggerRequest], dlp.JobTrigger]:
        r"""Return a callable for the update job trigger method over gRPC.

        Updates a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Returns:
            Callable[[~.UpdateJobTriggerRequest],
                    ~.JobTrigger]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_job_trigger" not in self._stubs:
            self._stubs["update_job_trigger"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/UpdateJobTrigger",
                request_serializer=dlp.UpdateJobTriggerRequest.serialize,
                response_deserializer=dlp.JobTrigger.deserialize,
            )
        return self._stubs["update_job_trigger"]

    @property
    def hybrid_inspect_job_trigger(
        self,
    ) -> Callable[[dlp.HybridInspectJobTriggerRequest], dlp.HybridInspectResponse]:
        r"""Return a callable for the hybrid inspect job trigger method over gRPC.

        Inspect hybrid content and store findings to a
        trigger. The inspection will be processed
        asynchronously. To review the findings monitor the jobs
        within the trigger.

        Returns:
            Callable[[~.HybridInspectJobTriggerRequest],
                    ~.HybridInspectResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "hybrid_inspect_job_trigger" not in self._stubs:
            self._stubs["hybrid_inspect_job_trigger"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/HybridInspectJobTrigger",
                request_serializer=dlp.HybridInspectJobTriggerRequest.serialize,
                response_deserializer=dlp.HybridInspectResponse.deserialize,
            )
        return self._stubs["hybrid_inspect_job_trigger"]

    @property
    def get_job_trigger(self) -> Callable[[dlp.GetJobTriggerRequest], dlp.JobTrigger]:
        r"""Return a callable for the get job trigger method over gRPC.

        Gets a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Returns:
            Callable[[~.GetJobTriggerRequest],
                    ~.JobTrigger]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_job_trigger" not in self._stubs:
            self._stubs["get_job_trigger"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/GetJobTrigger",
                request_serializer=dlp.GetJobTriggerRequest.serialize,
                response_deserializer=dlp.JobTrigger.deserialize,
            )
        return self._stubs["get_job_trigger"]

    @property
    def list_job_triggers(
        self,
    ) -> Callable[[dlp.ListJobTriggersRequest], dlp.ListJobTriggersResponse]:
        r"""Return a callable for the list job triggers method over gRPC.

        Lists job triggers.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Returns:
            Callable[[~.ListJobTriggersRequest],
                    ~.ListJobTriggersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_job_triggers" not in self._stubs:
            self._stubs["list_job_triggers"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ListJobTriggers",
                request_serializer=dlp.ListJobTriggersRequest.serialize,
                response_deserializer=dlp.ListJobTriggersResponse.deserialize,
            )
        return self._stubs["list_job_triggers"]

    @property
    def delete_job_trigger(
        self,
    ) -> Callable[[dlp.DeleteJobTriggerRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete job trigger method over gRPC.

        Deletes a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Returns:
            Callable[[~.DeleteJobTriggerRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_job_trigger" not in self._stubs:
            self._stubs["delete_job_trigger"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/DeleteJobTrigger",
                request_serializer=dlp.DeleteJobTriggerRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_job_trigger"]

    @property
    def activate_job_trigger(
        self,
    ) -> Callable[[dlp.ActivateJobTriggerRequest], dlp.DlpJob]:
        r"""Return a callable for the activate job trigger method over gRPC.

        Activate a job trigger. Causes the immediate execute
        of a trigger instead of waiting on the trigger event to
        occur.

        Returns:
            Callable[[~.ActivateJobTriggerRequest],
                    ~.DlpJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "activate_job_trigger" not in self._stubs:
            self._stubs["activate_job_trigger"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ActivateJobTrigger",
                request_serializer=dlp.ActivateJobTriggerRequest.serialize,
                response_deserializer=dlp.DlpJob.deserialize,
            )
        return self._stubs["activate_job_trigger"]

    @property
    def create_dlp_job(self) -> Callable[[dlp.CreateDlpJobRequest], dlp.DlpJob]:
        r"""Return a callable for the create dlp job method over gRPC.

        Creates a new job to inspect storage or calculate
        risk metrics. See
        https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.
        When no InfoTypes or CustomInfoTypes are specified in
        inspect jobs, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        Returns:
            Callable[[~.CreateDlpJobRequest],
                    ~.DlpJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_dlp_job" not in self._stubs:
            self._stubs["create_dlp_job"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/CreateDlpJob",
                request_serializer=dlp.CreateDlpJobRequest.serialize,
                response_deserializer=dlp.DlpJob.deserialize,
            )
        return self._stubs["create_dlp_job"]

    @property
    def list_dlp_jobs(
        self,
    ) -> Callable[[dlp.ListDlpJobsRequest], dlp.ListDlpJobsResponse]:
        r"""Return a callable for the list dlp jobs method over gRPC.

        Lists DlpJobs that match the specified filter in the
        request. See
        https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        Returns:
            Callable[[~.ListDlpJobsRequest],
                    ~.ListDlpJobsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_dlp_jobs" not in self._stubs:
            self._stubs["list_dlp_jobs"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ListDlpJobs",
                request_serializer=dlp.ListDlpJobsRequest.serialize,
                response_deserializer=dlp.ListDlpJobsResponse.deserialize,
            )
        return self._stubs["list_dlp_jobs"]

    @property
    def get_dlp_job(self) -> Callable[[dlp.GetDlpJobRequest], dlp.DlpJob]:
        r"""Return a callable for the get dlp job method over gRPC.

        Gets the latest state of a long-running DlpJob.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and https://cloud.google.com/dlp/docs/compute-risk-
        analysis to learn more.

        Returns:
            Callable[[~.GetDlpJobRequest],
                    ~.DlpJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_dlp_job" not in self._stubs:
            self._stubs["get_dlp_job"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/GetDlpJob",
                request_serializer=dlp.GetDlpJobRequest.serialize,
                response_deserializer=dlp.DlpJob.deserialize,
            )
        return self._stubs["get_dlp_job"]

    @property
    def delete_dlp_job(self) -> Callable[[dlp.DeleteDlpJobRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete dlp job method over gRPC.

        Deletes a long-running DlpJob. This method indicates
        that the client is no longer interested in the DlpJob
        result. The job will be cancelled if possible.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and https://cloud.google.com/dlp/docs/compute-risk-
        analysis to learn more.

        Returns:
            Callable[[~.DeleteDlpJobRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_dlp_job" not in self._stubs:
            self._stubs["delete_dlp_job"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/DeleteDlpJob",
                request_serializer=dlp.DeleteDlpJobRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_dlp_job"]

    @property
    def cancel_dlp_job(self) -> Callable[[dlp.CancelDlpJobRequest], empty_pb2.Empty]:
        r"""Return a callable for the cancel dlp job method over gRPC.

        Starts asynchronous cancellation on a long-running
        DlpJob. The server makes a best effort to cancel the
        DlpJob, but success is not guaranteed.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and https://cloud.google.com/dlp/docs/compute-risk-
        analysis to learn more.

        Returns:
            Callable[[~.CancelDlpJobRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_dlp_job" not in self._stubs:
            self._stubs["cancel_dlp_job"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/CancelDlpJob",
                request_serializer=dlp.CancelDlpJobRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["cancel_dlp_job"]

    @property
    def create_stored_info_type(
        self,
    ) -> Callable[[dlp.CreateStoredInfoTypeRequest], dlp.StoredInfoType]:
        r"""Return a callable for the create stored info type method over gRPC.

        Creates a pre-built stored infoType to be used for
        inspection. See
        https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Returns:
            Callable[[~.CreateStoredInfoTypeRequest],
                    ~.StoredInfoType]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_stored_info_type" not in self._stubs:
            self._stubs["create_stored_info_type"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/CreateStoredInfoType",
                request_serializer=dlp.CreateStoredInfoTypeRequest.serialize,
                response_deserializer=dlp.StoredInfoType.deserialize,
            )
        return self._stubs["create_stored_info_type"]

    @property
    def update_stored_info_type(
        self,
    ) -> Callable[[dlp.UpdateStoredInfoTypeRequest], dlp.StoredInfoType]:
        r"""Return a callable for the update stored info type method over gRPC.

        Updates the stored infoType by creating a new
        version. The existing version will continue to be used
        until the new version is ready. See
        https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Returns:
            Callable[[~.UpdateStoredInfoTypeRequest],
                    ~.StoredInfoType]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_stored_info_type" not in self._stubs:
            self._stubs["update_stored_info_type"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/UpdateStoredInfoType",
                request_serializer=dlp.UpdateStoredInfoTypeRequest.serialize,
                response_deserializer=dlp.StoredInfoType.deserialize,
            )
        return self._stubs["update_stored_info_type"]

    @property
    def get_stored_info_type(
        self,
    ) -> Callable[[dlp.GetStoredInfoTypeRequest], dlp.StoredInfoType]:
        r"""Return a callable for the get stored info type method over gRPC.

        Gets a stored infoType.
        See https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Returns:
            Callable[[~.GetStoredInfoTypeRequest],
                    ~.StoredInfoType]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_stored_info_type" not in self._stubs:
            self._stubs["get_stored_info_type"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/GetStoredInfoType",
                request_serializer=dlp.GetStoredInfoTypeRequest.serialize,
                response_deserializer=dlp.StoredInfoType.deserialize,
            )
        return self._stubs["get_stored_info_type"]

    @property
    def list_stored_info_types(
        self,
    ) -> Callable[[dlp.ListStoredInfoTypesRequest], dlp.ListStoredInfoTypesResponse]:
        r"""Return a callable for the list stored info types method over gRPC.

        Lists stored infoTypes.
        See https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Returns:
            Callable[[~.ListStoredInfoTypesRequest],
                    ~.ListStoredInfoTypesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_stored_info_types" not in self._stubs:
            self._stubs["list_stored_info_types"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/ListStoredInfoTypes",
                request_serializer=dlp.ListStoredInfoTypesRequest.serialize,
                response_deserializer=dlp.ListStoredInfoTypesResponse.deserialize,
            )
        return self._stubs["list_stored_info_types"]

    @property
    def delete_stored_info_type(
        self,
    ) -> Callable[[dlp.DeleteStoredInfoTypeRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete stored info type method over gRPC.

        Deletes a stored infoType.
        See https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Returns:
            Callable[[~.DeleteStoredInfoTypeRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_stored_info_type" not in self._stubs:
            self._stubs["delete_stored_info_type"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/DeleteStoredInfoType",
                request_serializer=dlp.DeleteStoredInfoTypeRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_stored_info_type"]

    @property
    def hybrid_inspect_dlp_job(
        self,
    ) -> Callable[[dlp.HybridInspectDlpJobRequest], dlp.HybridInspectResponse]:
        r"""Return a callable for the hybrid inspect dlp job method over gRPC.

        Inspect hybrid content and store findings to a job.
        To review the findings, inspect the job. Inspection will
        occur asynchronously.

        Returns:
            Callable[[~.HybridInspectDlpJobRequest],
                    ~.HybridInspectResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "hybrid_inspect_dlp_job" not in self._stubs:
            self._stubs["hybrid_inspect_dlp_job"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/HybridInspectDlpJob",
                request_serializer=dlp.HybridInspectDlpJobRequest.serialize,
                response_deserializer=dlp.HybridInspectResponse.deserialize,
            )
        return self._stubs["hybrid_inspect_dlp_job"]

    @property
    def finish_dlp_job(self) -> Callable[[dlp.FinishDlpJobRequest], empty_pb2.Empty]:
        r"""Return a callable for the finish dlp job method over gRPC.

        Finish a running hybrid DlpJob. Triggers the
        finalization steps and running of any enabled actions
        that have not yet run.

        Returns:
            Callable[[~.FinishDlpJobRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "finish_dlp_job" not in self._stubs:
            self._stubs["finish_dlp_job"] = self.grpc_channel.unary_unary(
                "/google.privacy.dlp.v2.DlpService/FinishDlpJob",
                request_serializer=dlp.FinishDlpJobRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["finish_dlp_job"]

    def close(self):
        self.grpc_channel.close()


__all__ = ("DlpServiceGrpcTransport",)
