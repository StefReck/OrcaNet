from unittest import TestCase
from keras.layers import Input, Dense, Dropout, Activation, Convolution3D, BatchNormalization, MaxPooling3D,\
                         Convolution2D, MaxPooling2D
from keras.models import Model

from orcanet.builder_util.builders import BlockBuilder


class TestSequentialBuilder(TestCase):

    def test_input_names_and_shapes_full_model(self):
        body_defaults = {"type": "conv_block", "conv_dim": 3}
        head_defaults = {}
        builder = BlockBuilder(body_defaults, head_defaults)

        input_name = "test_input"
        input_shape = (4, 4, 4, 1)
        input_shapes = {input_name: input_shape}

        conv_layer_config = (
            {"filters": 3, },
            {"filters": 3, "pool_size": (2, 2, 2)},
            {"filters": 5, },
        )

        head_arch = "categorical"
        head_kwargs = {
            "output_name": "ts_output",
            "categories": 2,
        }

        model = builder.build(input_shapes, conv_layer_config, head_arch, head_kwargs)

        self.assertEqual([input_name, ], model.input_names)
        self.assertEqual(input_shape, model.input_shape[1:])

    def test_attach_layer_conv(self):
        inp = Input((6, 6, 1))
        body_defaults = {"type": "conv_block", "conv_dim": 2}
        layer_config = {"filters": 2, "pool_size": 2, "dropout": 0.2, "batchnorm": True, "kernel_reg": "l2"}

        builder = BlockBuilder(body_defaults, None)
        x = builder.attach_block(inp, layer_config)
        model = Model(inp, x)

        self.assertIsInstance(model.layers[1], Convolution2D)
        self.assertIsInstance(model.layers[2], BatchNormalization)
        self.assertIsInstance(model.layers[3], Activation)
        self.assertIsInstance(model.layers[4], MaxPooling2D)
        self.assertIsInstance(model.layers[5], Dropout)
        self.assertEqual(model.output_shape[1:], (3, 3, 2))

    def test_attach_layer_dense(self):
        inp = Input((3, 3, 1))
        body_defaults = {"type": "conv_block", "conv_dim": 2}
        layer_config = {"type": "dense_block", "units": 5, "dropout": 0.2, "batchnorm": True}

        builder = BlockBuilder(body_defaults, None)
        x = builder.attach_block(inp, layer_config)
        model = Model(inp, x)

        self.assertIsInstance(model.layers[1], Dense)
        self.assertIsInstance(model.layers[2], BatchNormalization)
        self.assertIsInstance(model.layers[3], Activation)
        self.assertIsInstance(model.layers[4], Dropout)
        self.assertEqual(model.output_shape[1:], (3, 3, 5))

    def test_attach_layer_wrong_layer_config_conv_block(self):
        inp = Input((3, 3, 1))
        layer_config = {"type": "conv_block", "filters": 2, "units": 5}
        builder = BlockBuilder(None, None)

        with self.assertRaises(TypeError):
            builder.attach_block(inp, layer_config)

    def test_attach_layer_wrong_layer_config_dense_block(self):
        inp = Input((3, 3, 1))
        layer_config = {"type": "dense_block", "filters": 2, "units": 5}
        builder = BlockBuilder(None, None)

        with self.assertRaises(TypeError):
            builder.attach_block(inp, layer_config)
