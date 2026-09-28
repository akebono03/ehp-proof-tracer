import pytest

from repository_generator_applicability_selection import (
  RepositoryGeneratorApplicabilitySelection,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def test_phase104_2b_selection_preserves_source_result_and_candidate_identity():
  data = build_grouped_fixture()

  selection = (
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=(
        data[
          "candidates"
        ][0],
        data[
          "candidates"
        ][2],
      ),
    )
  )

  assert (
    selection.applicability_result
    is data[
      "result"
    ]
  )

  assert (
    selection.candidates[
      0
    ]
    is data[
      "candidates"
    ][0]
  )

  assert (
    selection.candidates[
      1
    ]
    is data[
      "candidates"
    ][2]
  )


def test_phase104_2b_empty_selection_is_valid():
  data = build_grouped_fixture()

  selection = (
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=(),
    )
  )

  assert selection.candidates == ()


def test_phase104_2b_selection_rejects_non_applicability_result():
  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=object(),
      candidates=(),
    )


def test_phase104_2b_selection_requires_candidate_tuple():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match="candidates must be a tuple",
  ):
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=[],
    )


def test_phase104_2b_selection_rejects_non_candidate_member():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "candidates must contain only "
      "RepositoryProofScopeApplicabilityCandidate objects"
    ),
  ):
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=(
        object(),
      ),
    )


def test_phase104_2b_selection_rejects_equal_or_similar_foreign_identity():
  data = build_grouped_fixture()
  foreign_data = build_grouped_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "each candidate must be an original candidate "
      "from applicability_result"
    ),
  ):
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=(
        foreign_data[
          "candidates"
        ][0],
      ),
    )


def test_phase104_2b_selection_rejects_duplicate_candidate_identity():
  data = build_grouped_fixture()

  candidate = data[
    "candidates"
  ][0]

  with pytest.raises(
    ValueError,
    match=(
      "candidates must not contain duplicate "
      "candidate identities"
    ),
  ):
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=(
        candidate,
        candidate,
      ),
    )


def test_phase104_2b_selection_preserves_discovery_order():
  data = build_grouped_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "candidates must preserve applicability_result "
      "candidate order"
    ),
  ):
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=data[
        "result"
      ],
      candidates=(
        data[
          "candidates"
        ][2],
        data[
          "candidates"
        ][0],
      ),
    )
