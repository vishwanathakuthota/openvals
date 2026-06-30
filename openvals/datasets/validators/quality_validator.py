from collections import Counter
MAX_HEALTH_SCORE = 100
def validate_quality(dataset):

    warnings = []

    empty_prompts = 0
    empty_outputs = 0

    short_prompts = 0
    short_outputs = 0

    duplicate_count = 0

    prompt_list = []

    # =====================================================
    # RECORD CHECKS
    # =====================================================

    for index, sample in enumerate(dataset):

        prompt = str(
            sample.get("prompt")
            or sample.get("input")
            or ""
        ).strip()

        expected = str(
            sample.get("expected_output")
            or sample.get("output")
            or ""
        ).strip()

        # ==============================================
        # EMPTY PROMPTS
        # ==============================================

        if not prompt:

            empty_prompts += 1

            warnings.append(
                f"Record {index}: empty prompt"
            )

        # ==============================================
        # EMPTY OUTPUTS
        # ==============================================

        if not expected:

            empty_outputs += 1

            warnings.append(
                f"Record {index}: empty expected_output"
            )

        # ==============================================
        # SHORT PROMPTS
        # ==============================================

        if prompt and len(prompt) < 5:

            short_prompts += 1

        # ==============================================
        # SHORT OUTPUTS
        # ==============================================

        if expected and len(expected) < 2:

            short_outputs += 1

        # ==============================================
        # DUPLICATES
        # ==============================================

        if prompt:

            prompt_list.append(
                prompt.lower()
            )

    # =====================================================
    # DUPLICATE DETECTION
    # =====================================================

    prompt_counts = Counter(
        prompt_list
    )

    duplicates = {

        prompt: count

        for prompt, count

        in prompt_counts.items()

        if count > 1

    }

    duplicate_count = len(
        duplicates
    )

    # =====================================================
    # DATASET HEALTH SCORE
    # =====================================================

    health_score = MAX_HEALTH_SCORE

    health_score -= (
        empty_prompts * 10
    )

    health_score -= (
        empty_outputs * 10
    )

    health_score -= (
        duplicate_count * 5
    )

    health_score -= (
        short_prompts * 2
    )

    health_score -= (
        short_outputs * 2
    )

    health_score = max(
        0,
        health_score
    )

    # =====================================================
    # HEALTH STATUS
    # =====================================================

    if health_score >= 90:

        status = "Healthy"

    elif health_score >= 70:

        status = "Acceptable"

    elif health_score >= 50:

        status = "Needs Review"

    else:

        status = "Poor"

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "health_score": health_score,

        "status": status,

        "empty_prompts": empty_prompts,

        "empty_outputs": empty_outputs,

        "short_prompts": short_prompts,

        "short_outputs": short_outputs,

        "duplicate_prompts": duplicate_count,

        "duplicates": duplicates,

        "warnings": warnings

    }