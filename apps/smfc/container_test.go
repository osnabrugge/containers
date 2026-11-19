package main

import (
	_ "embed"
	"testing"

	helpers "github.com/home-operations/containers/tests"
)

//go:embed hwmon_test.py
var sensorTests string

func Test(t *testing.T) {
	image := helpers.GetTestImage("ghcr.io/osnabrugge/smfc:6.5.0-homeops.1")
	helpers.RequireCommandSucceeds(t, image, nil, "python3", "-B", "-c", sensorTests)
	helpers.RequireFileExists(t, image, "/usr/share/licenses/smfc/LICENSE")
}
