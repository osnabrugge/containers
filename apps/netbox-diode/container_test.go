package main

import (
	"testing"

	helpers "github.com/home-operations/containers/tests"
)

func Test(t *testing.T) {
	image := helpers.GetTestImage("ghcr.io/osnabrugge/netbox-diode:4.7.4")
	helpers.RequireCommandSucceeds(t, image, nil, "/opt/netbox/venv/bin/python", "-c",
		"import importlib.metadata as m, os, grpc; from google.protobuf import __version__; "+
			"assert os.geteuid() != 0; "+
			"assert m.version('netboxlabs-diode-netbox-plugin') == '1.19.0'; "+
			"print('Non-root plugin and native dependency imports passed', grpc.__version__, __version__)")
	helpers.RequireCommandSucceeds(t, image, nil, "/usr/local/bin/uv", "pip", "check",
		"--python", "/opt/netbox/venv/bin/python")
	helpers.RequireFileExists(t, image, "/opt/netbox/docker-entrypoint.sh")
}
