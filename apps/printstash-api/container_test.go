package main

import (
	_ "embed"
	"testing"

	helpers "github.com/home-operations/containers/tests"
)

//go:embed capture_test.py
var captureTests string

func Test(t *testing.T) {
	image := helpers.GetTestImage("ghcr.io/osnabrugge/printstash-api:0.15.1-homeops.1")
	helpers.RequireCommandSucceeds(t, image, &helpers.ContainerConfig{
		Env: map[string]string{"VAULT_DATA_ROOT": "/tmp/printstash-capture-test"},
	}, "/app/.venv/bin/python", "-c", captureTests)
	helpers.RequireCommandSucceeds(t, image, nil, "/usr/local/bin/uv", "pip", "check",
		"--python", "/app/.venv/bin/python")
}
