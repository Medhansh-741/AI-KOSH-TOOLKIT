from app.engine.scoring.release_classifier import ReleaseClassificationEngine

def test_release_policy_overrides():
    # High stigma, High/Very High PRS -> Restricted
    res = ReleaseClassificationEngine.classify_release(
        cqi=80.0, prs=75, prs_band="Very High", sensitivity_class="high_stigma", differential_privacy_verified=False
    )
    assert res.classification == "Restricted"
    assert res.policy_override_applied is True

    # High stigma, Low PRS, not DP verified -> Controlled
    res = ReleaseClassificationEngine.classify_release(
        cqi=80.0, prs=10, prs_band="Low", sensitivity_class="high_stigma", differential_privacy_verified=False
    )
    assert res.classification == "Controlled"
    assert res.policy_override_applied is True

    # Critical sensitivity, Moderate PRS, DP verified -> standard matrix path -> Controlled
    res = ReleaseClassificationEngine.classify_release(
        cqi=80.0, prs=30, prs_band="Moderate", sensitivity_class="critical", differential_privacy_verified=True
    )
    assert res.classification == "Controlled"
    assert res.policy_override_applied is False

    # Critical sensitivity, Low PRS, DP verified -> standard matrix path -> Open
    res = ReleaseClassificationEngine.classify_release(
        cqi=80.0, prs=10, prs_band="Low", sensitivity_class="critical", differential_privacy_verified=True
    )
    assert res.classification == "Open"
    assert res.policy_override_applied is False

def test_release_standard_matrix():
    # CQI >= 70, PRS Low -> Open
    res = ReleaseClassificationEngine.classify_release(
        cqi=75.0, prs=10, prs_band="Low", sensitivity_class="standard"
    )
    assert res.classification == "Open"
    assert res.policy_override_applied is False

    # CQI >= 70, PRS Moderate -> Controlled
    res = ReleaseClassificationEngine.classify_release(
        cqi=75.0, prs=30, prs_band="Moderate", sensitivity_class="standard"
    )
    assert res.classification == "Controlled"
    assert res.policy_override_applied is False

    # PRS High/Very High -> Restricted regardless of CQI
    res = ReleaseClassificationEngine.classify_release(
        cqi=98.0, prs=50, prs_band="High", sensitivity_class="standard"
    )
    assert res.classification == "Restricted"
    assert res.policy_override_applied is False

    # CQI < 50, PRS Low -> Controlled
    res = ReleaseClassificationEngine.classify_release(
        cqi=45.0, prs=10, prs_band="Low", sensitivity_class="standard"
    )
    assert res.classification == "Controlled"
    assert res.policy_override_applied is False

    # CQI < 50, PRS Moderate/High/Very High -> Restricted
    res = ReleaseClassificationEngine.classify_release(
        cqi=45.0, prs=30, prs_band="Moderate", sensitivity_class="standard"
    )
    assert res.classification == "Restricted"
    assert res.policy_override_applied is False

    # Default (CQI 50-69, PRS Low/Moderate) -> Controlled
    res = ReleaseClassificationEngine.classify_release(
        cqi=60.0, prs=10, prs_band="Low", sensitivity_class="standard"
    )
    assert res.classification == "Controlled"
    assert res.policy_override_applied is False
