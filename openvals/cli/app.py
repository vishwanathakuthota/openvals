import profile

import typer
from pathlib import Path

from openvals import __version__

from openvals.datasets.loader import (
    load_builtin_dataset
)
from openvals.utils.system import get_system_profile
from openvals.models.discovery import discover_providers
from openvals.advisor.model_catalog import list_models

from openvals.datasets.metadata import (
    load_dataset_metadata
)
from openvals.datasets.validators.dataset_validator import (
    validate_dataset,
    validate_dataset_object,
    print_validation_report
)

from openvals.advisor.trust_readiness import compute_trust_readiness
from openvals.advisor.trust_workflow import (
    run_trust_workflow
)
from openvals.advisor.model_catalog import (
    get_model_catalog
)
from openvals.models.provider_config import (
    get_provider_env_vars
)

from openvals.datasets.registry import (
    DATASETS
)

from openvals.config.loader import (
    load_config
)
from openvals.advisor.recommendation_engine import (
    recommend_models
)
from openvals.diagnostics.doctor import run_doctor

from openvals.models.ollama_model import (
    OllamaModel
)
from openvals.models.discovery import discover_providers

from openvals.benchmarking.benchmark import (
    BenchmarkRunner
)

from openvals.recommendation.engine import (
    RecommendationEngine
)

from openvals.reporting.html_report import (
    generate_html_report
)
from openvals.reporting.sample_report import (
    generate_sample_report
)

from openvals.utils.paths import (
    create_output_structure
)
from openvals.explainability.trust_explain import (
    print_trust_workflow_explanation
)
from openvals.utils.system import (
    get_system_profile
)
# =========================================================
# TYPER APP
# =========================================================
app = typer.Typer(
    help=
    "OpenVals - "
    "Secure, Govern, scale and TRUST"

)
# =========================================================
# VERSION
# =========================================================
@app.command()
def version():
    """
    Show OpenVals version.
    """
    typer.echo(

        f"OpenVals v{__version__} "
        f"built by DrPinnacle "
        f"(https://drpinnacle.com) "
        f"Vishwanath Akuthota"
    )
# DOCTOR
@app.command("doctor")
def doctor_cli():
    """
    Show Environment Readiness.
    """
    report = run_doctor()

    system = report.get("system", {})
    gpu = system.get("gpu", {})
    disk = system.get("disk", {})
    typer.echo("\nOpenVals Doctor\n")

    typer.echo("Version")
    typer.echo(f"OpenVals : {report['version'].get('openvals')}")
    typer.echo(f"Python   : {report['version'].get('python')}")
    typer.echo(f"Platform : {report['version'].get('platform')}")
    typer.echo(f"Arch     : {report['version'].get('architecture')}")

    typer.echo("\nSystem")
    typer.echo(f"CPU Cores           : {system.get('cpu_count')}")
    typer.echo(f"Memory GB           : {system.get('memory_gb')}")
    typer.echo(f"Memory Available GB : {system.get('memory_available_gb')}")
    typer.echo(f"Memory Used         : {system.get('memory_percent_used')}%")
    
    typer.echo(f"Recommended Workers : {system.get('recommended_max_workers')}")

    typer.echo("\nGPU / Acceleration")
    typer.echo(f"Available           : {'Yes' if gpu.get('available') else 'No'}")
    typer.echo(f"Backend             : {gpu.get('backend', 'unknown')}")
    typer.echo(f"Vendor              : {gpu.get('vendor', 'unknown')}")
    devices = gpu.get("devices", [])
    if devices:
        for index, device in enumerate(devices, start=1):
            typer.echo(f"Device {index}            : {device.get('name', 'unknown')}")
            if device.get("memory_gb") is not None:
                typer.echo(f"GPU Memory GB       : {device.get('memory_gb')}")

    typer.echo("\nDisk")
    typer.echo(f"Disk Total GB       : {disk.get('total_gb')}")
    typer.echo(f"Disk Free GB        : {disk.get('free_gb')}")
    typer.echo(f"Disk Used           : {disk.get('percent_used')}%")

    typer.echo("\nProviders")
    for name, data in report["providers"].items():
        status = "OK" if data.get("configured") else "Missing"
        typer.echo(f"{name:<12} : {status}")

    typer.echo("\nModels")
    for model in report["installed_models"]:
        typer.echo(f"→ {model}")
    typer.echo(f"Installed Models    : {len(report['installed_models'])}")

    typer.echo("\nDatasets")
    for dataset in report["datasets"]:
        typer.echo(f"✓ {dataset}")

    typer.echo("\nConfigs")
    for config in report["configs"]:
        typer.echo(f"✓ {config}")

    typer.echo("\nOverall Health")
    if report["health"]["ready"]:
        typer.echo("Status              : Ready for Benchmarking")
    else:
        typer.echo("Status              : Setup incomplete")
        for issue in report["health"]["issues"]:
            typer.echo(f"⚠ {issue}")
#providers
@app.command("providers")
def providers_cli():
    """
    Show AI provider capability intelligence.
    """
    providers = discover_providers()
    typer.echo(
        "\nOpenVals Provider Intelligence\n"
    )
    for name, data in providers.items():
        typer.echo(
            f"{name.upper()}"
        )
        typer.echo(
            f"Type             : "
            f"{data.get('type', 'unknown')}"
        )
        typer.echo(
            f"Configured       : "
            f"{format_status(data.get('configured'))}"
        )
        typer.echo(
            f"Reachable        : "
            f"{format_status(data.get('reachable'))}"
        )
        typer.echo(
            f"Authenticated    : "
            f"{format_status(data.get('authenticated'))}"
        )
        typer.echo(
            f"Benchmark Ready  : "
            f"{format_status(data.get('benchmark_ready'))}"
        )
        models = data.get(
            "models",
            []
        )
        typer.echo(
            f"Models           : "
            f"{len(models)}"
        )
        if models:
            for model in models:
                typer.echo(
                    f"  → {model}"
                )
        issues = data.get(
            "issues",
            []
        )
        if issues:
            typer.echo(
                "Issues:"
            )
            for issue in issues:
                typer.echo(
                    f"  ⚠ {issue}"
                )
        typer.echo("")
# CLI utility functions
def format_status(value):
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "Unknown"
# System finding command
from openvals.diagnostics.system import (get_detailed_system_profile)
@app.command("system")
def system_cli():
    """
    Show OpenVals system diagnostics.
    """
    profile = get_detailed_system_profile()
    typer.echo("\nOpenVals System Diagnostics\n")
    typer.echo(
        f"CPU Cores           : "
        f"{profile.get('cpu_count')}"
    )
    typer.echo(
        f"Memory GB           : "
        f"{profile.get('memory_gb')}"
    )
    typer.echo(
        f"Memory Available GB : "
        f"{profile.get('memory_available_gb')}"
    )
    typer.echo(
        f"Memory Used         : "
        f"{profile.get('memory_percent_used')}%"
    )
    typer.echo(
        f"Recommended Workers : "
        f"{profile.get('recommended_max_workers')}"
    )
    typer.echo(
        f"Mode                : "
        f"{profile.get('mode')}"
    )
    # GPU
    gpu = profile.get("gpu", {})
    typer.echo("\nGPU / Acceleration")
    typer.echo(
        f"Available           : "
        f"{'Yes' if gpu.get('available') else 'No'}"
    )
    typer.echo(
        f"Backend             : "
        f"{gpu.get('backend', 'unknown')}"
    )
    typer.echo(
        f"Vendor              : "
        f"{gpu.get('vendor') or 'unknown'}"
    )

    devices = gpu.get("devices", [])

    if devices:
        for index, device in enumerate(
            devices,
            start=1,
        ):
            typer.echo(
                f"Device {index}            : "
                f"{device.get('name', 'unknown')}"
            )

            if device.get("memory_gb") is not None:
                typer.echo(
                    f"GPU Memory GB       : "
                    f"{device.get('memory_gb')}"
                )
    # DISK
    disk = profile.get("disk", {})
    typer.echo("\nDisk")
    typer.echo(
        f"Total GB            : "
        f"{disk.get('total_gb')}"
    )
    typer.echo(
        f"Free GB             : "
        f"{disk.get('free_gb')}"
    )
    typer.echo(
        f"Used                : "
        f"{disk.get('percent_used')}%"
    )
# BENCHMARK
@app.command("benchmark")
def benchmark(
    dataset: str = typer.Option(
        ...,
        help="Dataset name"
    ),

    config: str = typer.Option(
        None,
        help="Config preset"
    ),

    models: str = typer.Option(
        ...,
        help="Comma-separated model names"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable detailed metric debugging"
    ),
    parallel: bool = typer.Option(
        False,
        "--parallel",
        help="Run benchmarks in parallel (multi-threaded)"
    ),
    max_workers: int = typer.Option(
        3,
        "--max-workers",
        help="Max workers for parallel execution"
    ),

    report: bool = typer.Option(
        True,
        help="Generate HTML report"
    ),

    output: str = typer.Option(
        "outputs/report.html",
        help="Output HTML report file"
    )

):

    """
    Run OpenVals benchmark.
    """
    typer.echo(

        f"\n🚀 OpenVals AI Trust Platform "
        f"Starting... (v{__version__})\n"

    )
    # =====================================================
    # CREATE OUTPUT STRUCTURE
    # =====================================================
    create_output_structure()
    output_path = Path(output)
    if not output_path.parent.exists():
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
    # =====================================================
    # LOAD DATASET
    # =====================================================
    dataset_data = load_builtin_dataset(
        dataset
    )

    metadata = load_dataset_metadata(
        dataset
    )

    if config:

        cfg = load_config(config)

        weights = cfg["weights"]

        typer.echo(
            f"⚙️ Config Loaded : {config}"
        )

    else:

        weights = metadata[
            "recommended_weights"
        ]

    typer.echo("Dataset Loaded")

    typer.echo(
        f"Dataset : {metadata['name']}"
    )

    typer.echo(
        f"Domain  : {metadata['domain']}"
    )

    typer.echo(
        f"Version : {metadata['version']}\n"
    )

    # =====================================================
    # LOAD MODELS
    # =====================================================

    model_names = [

        m.strip()

        for m in models.split(",")

    ]

    loaded_models = {}

    for model_name in model_names:

        try:

            loaded_models[
                model_name
            ] = OllamaModel(model_name)

        except Exception as e:

            typer.echo(

                f"❌ Failed to load model "
                f"{model_name}: {str(e)}"

            )

    if not loaded_models:

        typer.echo(
            "\n❌ No models loaded successfully."
        )

        raise typer.Exit()

    typer.echo(

        f"Models Loaded: "
        f"{', '.join(loaded_models.keys())}\n"
    )
    if parallel:
        typer.echo(
            f"⚡ Running benchmarks in parallel "
            f"with max workers: {max_workers}\n"
        )
    if debug:
        typer.echo(
            "Debug mode enabled\n"
        )
    # =====================================================
    # RUN BENCHMARK
    # =====================================================
    runner = BenchmarkRunner(
        models=loaded_models,
        dataset=dataset_data,
        weights=weights,
        debug=debug,
        parallel=parallel,
        max_workers=max_workers
    )
    results = runner.run()
    # =====================================================
    # DRS RANKING
    # =====================================================
    ranking = sorted(

        [

            (
                model_name,
                results[model_name][
                    "drs_score"
                ]
            )

            for model_name in results

        ],

        key=lambda x: x[1],
        reverse=True

    )

    # =====================================================
    # FINAL TABLE
    # =====================================================
    typer.echo(

        "\n=== MODEL BENCHMARK "
        "(DRS Ranked) ===\n"
    )
    print(

        f"{'Rank':<5} "
        f"{'Model':<15} "
        f"{'Acc':<8} "
        f"{'Sem':<8} "
        f"{'Fact':<8} "
        f"{'Rel':<8} "
        f"{'Safe':<8} "
        f"{'Cons':<8} "
        f"{'Var':<8} "
        f"{'HPI':<8} "
        f"{'Lat(ms)':<12} "
        f"{'DRS':<8}"

    )

    print("-" * 140)

    for rank, (

        model_name,
        drs_score

    ) in enumerate(

        ranking,
        start=1

    ):

        metrics = results[
            model_name
        ]["metrics"]

        print(

            f"{rank:<5} "
            f"{model_name:<15} "
            f"{metrics.get('accuracy', 0):<8.3f} "
            f"{metrics.get('semantic', 0):<8.3f} "
            f"{metrics.get('factuality', 0):<8.3f} "
            f"{metrics.get('reliability', 0):<8.3f} "
            f"{metrics.get('safety', 0):<8.3f} "
            f"{metrics.get('consistency', 0):<8.3f} "
            f"{metrics.get('variance', 0):<8.3f} "
            f"{metrics.get('hallucination', 0):<8.3f} "
            f"{metrics.get('latency', 0):<12.2f} "
            f"{drs_score:<8.3f}"

        )

    # =====================================================
    # RECOMMENDATION ENGINE
    # =====================================================

    engine = RecommendationEngine(
        results
    )

    recommendation = engine.recommend(
        use_case=dataset
    )

    # =====================================================
    # AI ADVISOR REPORT
    # =====================================================

    typer.echo(
        "\n=== AI ADVISOR REPORT ===\n"
    )

    typer.echo(

        f"✅ Recommended Model : "
        f"{recommendation.get('recommended_model', 'Unknown')}"

    )

    typer.echo(

        f"📊 Score             : "
        f"{recommendation.get('score', 0)}"

    )

    typer.echo(

        f"🧠 DRS               : "
        f"{recommendation.get('drs', 0)}"

    )

    typer.echo(

        f"🎯 Confidence        : "
        f"{recommendation.get('confidence', 0)}"

    )

    # =====================================================
    # HPI ANALYSIS
    # =====================================================

    recommended_model = recommendation.get(
        "recommended_model",
        "Unknown"
    )

    hallucination_score = results[
        recommended_model
    ]["metrics"].get(
        "hallucination",
        0
    )

    factuality_score = results[
        recommended_model
    ]["metrics"].get(
        "factuality",
        0
    )

    typer.echo(

        f"🧪 Hallucination Risk: "
        f"{hallucination_score:.3f}"

    )
    typer.echo(
        f"📚 Factuality Score  : "
        f"{factuality_score:.3f}"
    )

    if hallucination_score <= 0.20:

        typer.echo(
            "🟢 Low hallucination risk"
        )

    elif hallucination_score <= 0.40:

        typer.echo(
            "🟡 Moderate hallucination risk"
        )

    else:

        typer.echo(
            "🔴 High hallucination risk"
        )

    typer.echo("\n=== TRUST SUMMARY ===\n")
    drs = recommendation["drs"]
    if drs >= 0.85:
        typer.echo("🟢 Production Ready")
    elif drs >= 0.60:
        typer.echo("🟡 Caution Advised with Enterprise Capable")
    elif drs >= 0.35:
        typer.echo("🔴 Not Recommended Further Validation Recommended")
    else:
        typer.echo("⚠️ Critical Risk - Not Recommended")

    # =====================================================
    # WHY
    # =====================================================

    typer.echo("\nWhy:")

    typer.echo(

        f"→ {recommendation.get('reason', 'N/A')}"

    )

    # =====================================================
    # TRADEOFFS
    # =====================================================

    typer.echo("\nTrade-offs:")

    typer.echo(

        f"→ {recommendation.get('tradeoffs', 'N/A')}"

    )

    # =====================================================
    # RISKS
    # =====================================================

    typer.echo("\nRisks:")

    for risk in recommendation.get("risks", []):

        typer.echo(f"→ {risk}")

    # =====================================================
    # INSIGHTS
    # =====================================================

    if recommendation.get("insights"):

        typer.echo("\nInsights:")

        for insight in recommendation[
            "insights"
        ]:

            typer.echo(
                f"→ {insight}"
            )

    # =====================================================
    # GENERATE HTML REPORT
    # =====================================================

    if report:

        typer.echo(
            "\n📄 OpenVals AI Trust Assessment"
            "Evaluate • Benchmark • Trust Intelligence\n"
        )

        generate_html_report(
            results=results,
            recommendation=recommendation,
            output_file=str(output_path)
        )
        sample_report_path = (
            output_path.parent /
            f"sample_report_{dataset}.html"
        )
        generate_sample_report(
            results=results,
            output_file=str(sample_report_path)
        )

        typer.echo(
            "\n✅ OpenVals AI Trust Assessment Complete:"
        )
        typer.echo(
            f"📄 Dashboard saved to: {output_path.resolve()}"

        )
        typer.echo(
            f"📄 Sample report saved to: {sample_report_path.resolve()}"
        )

        typer.echo(
            "\n📊 Charts saved under:"
        )

        typer.echo(
            "📁 outputs/charts/"
        )


# =========================================================
# VALIDATE DATASET
# =========================================================

@app.command("validate-dataset")
def validate_dataset_cli(

    dataset: str = typer.Argument(
        ...,
        help="Dataset name or local dataset path"
    )

):

    """
    Validate an OpenVals built-in dataset or local JSON/CSV file.
    """

    typer.echo(
        f"\n🔍 Validating dataset: {dataset}"
    )

    try:
        if dataset in DATASETS:
            dataset_data = load_builtin_dataset(
                dataset
            )
            result = validate_dataset_object(
                dataset_data
            )
        else:
            result = validate_dataset(
                dataset
            )

        print_validation_report(
            result
        )

    except Exception as e:

        typer.echo(
            f"\n❌ Dataset validation failed: {str(e)}"
        )

        raise typer.Exit(code=1)

@app.command("trust-advisor")
def trust_advisor_cli(
    problem: str = typer.Option(
        None,
        "--problem",
        help="Problem statement or AI use case"
    ),

    benchmark: bool = typer.Option(
        False,
        "--benchmark",
        help="Run benchmark for recommended models"
    ),

    explain: bool = typer.Option(
        False,
        "--explain",
        help="Show detailed explanation of trust workflow results"
    ),

    mode: str = typer.Option(
        "standard",
        "--mode",
        help="Benchmark mode: quick, standard, full"
    ),

    file: str = typer.Option(
        None,
        "--file",
        help="Path to a text or JSON file describing the use case"
    ),

    top_k: int = typer.Option(
        3,
        "--top-k",
        help="Number of model recommendations"
    ),

    max_workers: int = typer.Option(
        None,
        "--max-workers",
        help="Max workers for parallel benchmarking (overrides auto-recommendation)"
    )

):
    """
    Generate a trust advisory profile for an AI use case.
    """
    try:
        if file:
            problem_text = load_use_case_from_file(
                file
            )
        elif problem:
            problem_text = problem
        else:
            typer.echo(
                "\n❌ Please provide --problem or --file"
            )
            raise typer.Exit(code=1)
        valid_modes = ["quick", "standard", "full"]
        if mode not in valid_modes:
            typer.echo(
                f"\n❌ Invalid mode: {mode}. "
                f"Choose from: {', '.join(valid_modes)}"
            )
            raise typer.Exit(code=1)
        if benchmark:
            workflow = run_trust_workflow(
                problem_text=problem_text,
                top_k=top_k,
                parallel=True,
                max_workers=max_workers,
                mode=mode,
                explain=explain
            )
            if explain:
                print_trust_workflow_explanation(workflow)
                return

            profile = workflow["profile"]
            tri = workflow["tri"]
            verdict = workflow["trust_verdict"]

            typer.echo("\n===> OpenVals Trust Advisor <====\n")

            typer.echo(f"Use Case           : {profile['use_case']}")
            typer.echo(f"Risk Level         : {profile['risk_level']}")
            typer.echo(f"Data Sensitivity   : {profile['data_sensitivity']}")
            typer.echo(f"Dataset            : {workflow['dataset']}")
            typer.echo(f"Config             : {workflow['config']}")
            typer.echo(f"TRI Score          : {tri['tri_score']}/100")
            typer.echo(f"Readiness          : {tri['readiness']}")

            typer.echo("\nBenchmark Result:")
            typer.echo(f"Best Model         : {workflow['best_model']}")
            typer.echo(f"Best DRS           : {workflow['best_drs']}")

            typer.echo("\nFinal Trust Verdict:")
            typer.echo(f"Verdict            : {verdict['verdict']}")
            typer.echo(f"Recommendation     : {verdict['recommendation']}")

            typer.echo("\nRequired Controls:")
            for control in verdict["required_controls"]:
                typer.echo(f"→ {control}")

            return

        profile = build_trust_profile(
            problem_text,
            top_k=top_k
        )

        tri = compute_trust_readiness(
            profile
        )



        typer.echo(
            "\n🛡️ OpenVals Trust Advisor\n"
        )

        typer.echo(
            f"Use Case           : "
            f"{profile['use_case']}"
        )

        typer.echo(
            f"Confidence         : "
            f"{profile['use_case_confidence']}"
        )

        typer.echo(
            f"Risk Level         : "
            f"{profile['risk_level']}"
        )

        typer.echo(
            f"Risk Reason        : "
            f"{profile['risk_reason']}"
        )

        typer.echo(
            f"Data Sensitivity   : "
            f"{profile['data_sensitivity']}"
        )

        typer.echo(
            f"Recommended Dataset: "
            f"{profile['recommended_dataset']}"
        )

        typer.echo(
            f"Recommended Config : "
            f"{profile['recommended_config']}"
        )

        typer.echo(
            f"Trust Status       : "
            f"{profile['trust_status']}"
        )

        typer.echo(
            f"TRI Score          : "
            f"{tri['tri_score']}/100"
        )

        typer.echo(
            f"Readiness          : "
            f"{tri['readiness']}"
        )

        typer.echo(
            "\nRecommended Metrics:"
        )

        for metric in profile[
            "recommended_metrics"
        ]:

            typer.echo(
                f"→ {metric}"
            )

        typer.echo(
            "\nRecommended Models:"
        )

        for idx, model in enumerate(
            profile["recommended_models"],
            start=1
        ):

            typer.echo(
                f"{idx}. {model['model']} "
                f"(MFS: {model['score']})"
            )

            typer.echo(
                f"   Why: {model['reason']}"
            )

        typer.echo(
            "\nValidation Strategy:"
        )

        for item in profile[
            "validation_strategy"
        ]:

            typer.echo(
                f"→ {item}"
            )

        typer.echo(
            "\nTRI Deductions:"
        )

        for item in tri[
            "deductions"
        ]:

            typer.echo(
                f"→ {item}"
            )

    except Exception as e:

        typer.echo(
            f"\n❌ Trust advisory failed: {str(e)}"
        )

        raise typer.Exit(code=1)
    
@app.command("recommend-model")
def recommend_model_cli(
    use_case: str = typer.Option(
        None,
        "--use-case",
        help="Use case profile, e.g. finance, cybersecurity, coding"
    ),
    problem: str = typer.Option(
        None,
        "--problem",
        help="Problem statement for the use case"
    ),
    file: str = typer.Option(
        None,
        "--file",
        help="Path to a text or JSON file describing the use case"
    ),
    top_k: int = typer.Option(
        3,
        "--top-k",
        help="Number of model recommendations"
    ),

    private_required: bool = typer.Option(
        False,
        "--private-required",
        help="Only recommend private-ready models"
    ),

    enterprise_required: bool = typer.Option(
        False,
        "--enterprise-required",
        help="Only recommend enterprise-ready models"
    )

):

    """
    Recommend the best model for a given use case.
    """
    try:

        # =================================================
        # LOAD PROBLEM STATEMENT OR FILE
        # =================================================
        use_case_text = ""
        if file:
            use_case_text = load_use_case_from_file(
                file
            )
        elif problem:
            use_case_text = problem

        # =================================================
        # AUTO-INFER USE CASE
        # =================================================

        if not use_case and use_case_text:

            analysis = analyze_use_case_text(
                use_case_text
            )

            use_case = analysis[
                "use_case"
            ]

            typer.echo(
                f"\n🧠 Inferred Use Case: "
                f"{use_case}"
            )

            typer.echo(
                f"Confidence: "
                f"{analysis['confidence']}"
            )

            typer.echo(
                f"Reason: "
                f"{analysis['reason']}\n"
            )

        # =================================================
        # VALIDATION
        # =================================================

        if not use_case:

            typer.echo(
                "\n❌ Please provide "
                "--use-case, --problem, or --file"
            )

            raise typer.Exit(code=1)

        # =================================================
        # RECOMMEND MODELS
        # =================================================

        result = recommend_models(
            use_case=use_case,
            top_k=top_k,
            private_required=private_required,
            enterprise_required=enterprise_required
        )

        typer.echo(
            f"\n🧭 OpenVals Model Advisor"
        )

        typer.echo(
            f"Use Case: {result['use_case']}"
        )

        typer.echo(
            f"Description: {result['description']}\n"
        )

        # =================================================
        # OPTIONAL ORIGINAL PROBLEM CONTEXT
        # =================================================

        if use_case_text:

            typer.echo(
                "Problem Context:"
            )

            typer.echo(
                f"{use_case_text}\n"
            )

        # =================================================
        # PRINT RECOMMENDATIONS
        # =================================================

        for idx, rec in enumerate(
            result["recommendations"],
            start=1
        ):

            typer.echo(
                f"{idx}. {rec['model']} "
                f"(MFS: {rec['score']})"
            )

            typer.echo(
                f"   Provider: {rec['provider']}"
            )

            typer.echo(
                f"   Type: {rec['model_type']}"
            )

            typer.echo(
                f"   Private Ready: {rec['private_ready']}"
            )

            typer.echo(
                f"   Enterprise Ready: {rec['enterprise_ready']}"
            )

            typer.echo(
                f"   Strengths: "
                f"{', '.join(rec['strengths'])}"
            )

            typer.echo(
                f"   Why: {rec['reason']}\n"
            )

    except Exception as e:

        typer.echo(
            f"\n❌ Model recommendation failed: {str(e)}"
        )

        raise typer.Exit(code=1)
    
# =========================================================
# MODELS
# =========================================================

@app.command("models")
def models_cli(

    installed_only: bool = typer.Option(
        True,
        "--installed-only/--all",
        help="Show installed Ollama models or all known catalog models"
    )

):

    """
    List models discovered by OpenVals.
    """

    catalog = get_model_catalog(
        installed_only=installed_only
    )

    typer.echo(
        "\n🤖 OpenVals Model Catalog\n"
    )

    print(
        f"{'Model':<25} "
        f"{'Provider':<12} "
        f"{'Type':<10} "
        f"{'Private':<10} "
        f"{'Enterprise':<12} "
        f"{'Dynamic':<10}"
    )

    print("-" * 90)

    for model_name, profile in catalog.items():

        print(
            f"{model_name:<25} "
            f"{profile.get('provider', 'unknown'):<12} "
            f"{profile.get('model_type', 'unknown'):<10} "
            f"{str(profile.get('private_ready', False)):<10} "
            f"{str(profile.get('enterprise_ready', False)):<12} "
            f"{str(profile.get('dynamic', False)):<10}"
        )    
# =========================================================
# DATASETS
# =========================================================
@app.command("datasets")
def datasets():

    """
    List available datasets.
    """

    typer.echo(

        "\n📦 Available "
        "OpenVals Datasets\n"

    )

    print(

        f"{'Dataset':<15} "
        f"{'Domain':<15} "
        f"{'Description'}"

    )

    print("-" * 70)

    for name, info in DATASETS.items():

        print(

            f"{name:<15} "
            f"{info['domain']:<15} "
            f"{info['description']}"

        )

# =========================================================
# ENTRYPOINT
# =========================================================

def main():
    app()

if __name__ == "__main__":
    main()