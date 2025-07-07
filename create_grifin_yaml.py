
import yaml

def prompt(field, default=None, required=False, allowed=None):
    while True:
        val = input(f"{field} [{default}]: ").strip()
        if not val and default is not None:
            return default
        if not val and required:
            print("This field is required.")
            continue
        if allowed and val not in allowed:
            print(f"Allowed values: {allowed}")
            continue
        return val

def get_growth_options():
    print("\n--- GROWTH OPTIONS ---\n")
    growth_zones = {}
    min_slope = prompt("Minimum stream slope (deg)", default="5")
    if min_slope:
        growth_zones["min_stream_slope"] = float(min_slope)

    growth_volumes = {}
    print("\n--- Select ONE: area_growth, length_growth, or point_source_volumes_file ---")
    use_area = prompt("Use area_growth? (yes/no)", default="no", allowed=["yes", "no"]) == "yes"
    use_length = prompt("Use length_growth? (yes/no)", default="yes", allowed=["yes", "no"]) == "yes"
    use_point_source = prompt("Use point_source_volumes_file? (yes/no)", default="no", allowed=["yes", "no"]) == "yes"

    if use_area:
        area_growth = {
            "area_growth_factor": float(prompt("Area growth factor", default="1.0")),
            "area_power": float(prompt("Area power", default="1.0"))
        }
        growth_volumes["area_growth"] = area_growth

    if use_length:
        length_growth = {
            "length_growth_factor": float(prompt("Length growth factor", default="2.0")),
            "length_power": float(prompt("Length power", default="1.0"))
        }
        growth_volumes["length_growth"] = length_growth

    if use_point_source:
        file = prompt("Path to point_source_volumes_file (CSV)", required=True)
        growth_volumes["point_source_volumes_file"] = file

    return {
        "growth_zones": growth_zones,
        "growth_volumes": growth_volumes
    }

def get_hl_options():
    print("\n--- HL OPTIONS ---\n")
    angle = float(prompt("Minimum reach angle (degrees)", default="25", required=True))
    return {
        "min_reach_angle": angle
    }

def get_inundation_options():
    print("\n--- INUNDATION OPTIONS ---\n")
    options = {}
    flowtype = prompt("Flow type", default="debrisflow", allowed=["debrisflow", "lahar", "rockavalanche", "custom"])
    options["flowtype"] = flowtype

    if flowtype == "custom":
        options["xsec_alpha1"] = float(prompt("Custom xsec_alpha1", required=True))
        options["plan_alpha2"] = float(prompt("Custom plan_alpha2", required=True))

    use_csv = prompt("Use user_specified_volumes_file? (yes/no)", default="no", allowed=["yes", "no"]) == "yes"
    if use_csv:
        options["user_specified_volumes_file"] = prompt("Path to volumes CSV", required=True)

    use_alt_dem = prompt("Use alternate DEM for cross sections? (yes/no)", default="no", allowed=["yes", "no"]) == "yes"
    if use_alt_dem:
        options["xsec_demfilename"] = prompt("Path to alternate DEM", required=True)

    hbar = prompt("Enable hbar constraint? (yes/no)", default="no", allowed=["yes", "no"])
    options["hbar"] = hbar

    return options

def main():
    print("\n--- GRIFIN YAML Creator ---\n")

    setup = {
        'title': prompt("Title (optional)", default=''),
        'demfilename': prompt("DEM filename (e.g., input/DEM.tif)", required=True),
        'compute_taudem_grids': prompt("Compute TauDEM grids", default="if_absent", allowed=["yes", "no", "if_absent"]),
        'dest_dir': prompt("Output directory", required=True),
        'num_procs': int(prompt("Number of processes", default="1"))
    }

    options = {
        'hl': prompt("Enable H/L Tool?", default="no", allowed=["yes", "no"]),
        'growth': prompt("Enable Growth Tool?", default="yes", allowed=["yes", "no"]),
        'inundation': prompt("Enable Inundation Tool?", default="yes", allowed=["yes", "no"]),
    }

    config = {'setup': setup, 'options': options}

    if options["growth"] == "yes":
        config["growth_options"] = get_growth_options()

    if options["hl"] == "yes":
        config["hl_options"] = get_hl_options()

    if options["inundation"] == "yes":
        config["inundation_options"] = get_inundation_options()

    output_file = prompt("YAML output filename", default="settings.yaml")

    with open(output_file, 'w') as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"\nYAML file saved to: {output_file}")

if __name__ == "__main__":
    main()
