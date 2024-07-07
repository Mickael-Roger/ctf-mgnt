{ #lib
 python3Packages
}:

python3Packages.buildPythonApplication rec {
    pname = "ctf-mngt";
    version = "0.1.0";
    format = "other";

    propagatedBuildInputs = [
        # List of dependencies
        python3Packages.argparse
    ];

    src = ./.;

    dontUnpack = true;
    installPhase = ''
        install -Dm755 ${./${pname}} $out/bin/${pname}
    '';
}
