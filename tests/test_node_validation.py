from meshtastic.protobuf import config_pb2, channel_pb2

from baymesh import node_validation, firmware_versions


class TestNodeValidationChecks(object):
    """Test suite for node validation checks."""

    @staticmethod
    def _assert_success(
        recommendation: node_validation.Recommendation | None, message=None
    ):
        """Checks for a successful validation run."""
        assert recommendation is None, (
            message or "Expected no recommendation but found one."
        )

    @staticmethod
    def _assert_recommendation(
        recommendation: node_validation.Recommendation | None,
        severity: node_validation.RecommendationSeverity,
        message=None,
    ):
        """Checks for a successful validation run."""
        assert recommendation is not None, (
            message or "Expected a recommendation but found none."
        )
        if severity:
            assert recommendation.severity == severity, (
                message or "Severity does not match expected value."
            )

    def test_check_user_long_name(self):
        """Exercise node long name validation."""
        assert node_validation._check_user_long_name("This should pass") is None
        # Error if the device has a name that looks like a default.
        assert node_validation._check_user_long_name("Meshtastic 3cc8") is not None

    def test_check_lora_region(self):
        """Exercise node region validation."""
        self._assert_success(
            node_validation._check_lora_region(
                region=config_pb2.Config.LoRaConfig.RegionCode.US
            )
        )
        self._assert_recommendation(
            node_validation._check_lora_region(
                region=config_pb2.Config.LoRaConfig.RegionCode.EU_433
            ),
            severity=node_validation.RecommendationSeverity.ERROR,
        )

    def test_check_lora_preset(self):
        """Exercise node lora preset validation."""
        self._assert_success(
            node_validation._check_lora_preset(
                use_preset=True,
                modem_preset=config_pb2.Config.LoRaConfig.ModemPreset.MEDIUM_SLOW,
            )
        )
        self._assert_recommendation(
            node_validation._check_lora_preset(
                use_preset=True,
                modem_preset=config_pb2.Config.LoRaConfig.ModemPreset.LONG_FAST,
            ),
            severity=node_validation.RecommendationSeverity.ERROR,
        )
        self._assert_recommendation(
            node_validation._check_lora_preset(
                use_preset=False,
                modem_preset=config_pb2.Config.LoRaConfig.ModemPreset.MEDIUM_SLOW,
            ),
            severity=node_validation.RecommendationSeverity.ERROR,
        )

    def test_check_lora_hop_limit(self):
        """Exercise node lora hop limit validation."""
        self._assert_success(node_validation._check_lora_hop_limit(3))
        self._assert_recommendation(
            node_validation._check_lora_hop_limit(2),
            severity=node_validation.RecommendationSeverity.WARNING,
        )
        self._assert_recommendation(
            node_validation._check_lora_hop_limit(4),
            severity=node_validation.RecommendationSeverity.WARNING,
        )

    def test_check_device_role(self):
        """Exercise node device role validation."""
        self._assert_success(
            node_validation._check_device_role(config_pb2.Config.DeviceConfig.Role.CLIENT)
        )
        self._assert_success(
            node_validation._check_device_role(
                config_pb2.Config.DeviceConfig.Role.CLIENT_MUTE
            )
        )
        self._assert_success(
            node_validation._check_device_role(
                config_pb2.Config.DeviceConfig.Role.CLIENT_HIDDEN
            )
        )
        self._assert_success(
            node_validation._check_device_role(
                config_pb2.Config.DeviceConfig.Role.ROUTER_LATE
            )
        )
        self._assert_recommendation(
            node_validation._check_device_role(
                config_pb2.Config.DeviceConfig.Role.ROUTER
            ),
            severity=node_validation.RecommendationSeverity.ERROR,
        )

    def test_check_module_telemetry_update_interval(self):
        """Exercise node module telemetry update intervals validation."""
        self._assert_success(
            node_validation._check_module_telemetry_update_interval(
                telemetry_type="device",
                update_interval=60 * 60,
            )
        )
        self._assert_recommendation(
            node_validation._check_module_telemetry_update_interval(
                telemetry_type="device",
                update_interval=60 * 30,
            ),
            severity=node_validation.RecommendationSeverity.WARNING,
        )

    def test_check_node_firmware_version(self):
        """Exercise node firmware version validation."""

        newer = firmware_versions.FirmwareVersion(
            major=2, minor=5, patch=18, commit_hash="89ebafc"
        )
        older = firmware_versions.FirmwareVersion(
            major=2, minor=5, patch=15, commit_hash="79da236"
        )
        self._assert_success(
            node_validation._check_node_firmware_version(
                node_firmware_version=newer,
                latest_firmware_version=older,
            )
        )
        self._assert_success(
            node_validation._check_node_firmware_version(
                node_firmware_version=newer,
                latest_firmware_version=newer,
            )
        )
        self._assert_recommendation(
            node_validation._check_node_firmware_version(
                node_firmware_version=older,
                latest_firmware_version=newer,
            ),
            severity=node_validation.RecommendationSeverity.ERROR,
        )

    def test_check_channels_mqtt_settings(self):
        """Exercise node channels mqtt setting validation."""

        valid_channel_0 = channel_pb2.Channel(
            index=0,
            settings=channel_pb2.ChannelSettings(
                downlink_enabled=False,
            ),
            role=channel_pb2.Channel.Role.PRIMARY,
        )
        valid_channel_list = [valid_channel_0]
        self._assert_success(
            node_validation._check_channels_mqtt_settings(channels=valid_channel_list)
        )

        invalid_channel_0 = channel_pb2.Channel(
            index=0,
            settings=channel_pb2.ChannelSettings(
                downlink_enabled=True,
            ),
            role=channel_pb2.Channel.Role.PRIMARY,
        )
        invalid_channel_list = [invalid_channel_0]
        self._assert_recommendation(
            node_validation._check_channels_mqtt_settings(channels=invalid_channel_list),
            severity=node_validation.RecommendationSeverity.ERROR,
        )
