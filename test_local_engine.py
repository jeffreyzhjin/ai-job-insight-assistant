from analysis_engine import EXAMPLE_JD, EXAMPLE_RESUME, MatchLevel, analyze_locally, result_to_markdown


def test_local_analysis_returns_core_sections() -> None:
    result = analyze_locally(EXAMPLE_JD, EXAMPLE_RESUME)
    assert result.position.category in {
        "Product Operations",
        "Business Analysis",
        "Strategy Analysis",
    }
    assert result.responsibilities
    assert result.required_qualifications
    assert result.interview_questions


def test_matches_do_not_invent_resume_evidence() -> None:
    result = analyze_locally(EXAMPLE_JD, EXAMPLE_RESUME)
    resume_sentences = EXAMPLE_RESUME.replace("\n", " ")
    for match in result.matches:
        if match.match_level != MatchLevel.GAP:
            assert match.resume_evidence in resume_sentences
        else:
            assert match.resume_evidence == "No direct evidence found in the provided resume."


def test_markdown_export_contains_verification_note() -> None:
    report = result_to_markdown(analyze_locally(EXAMPLE_JD, EXAMPLE_RESUME))
    assert "# AI Job Insight Report" in report
    assert "Verification note" in report
