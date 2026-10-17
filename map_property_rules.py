from dataclasses import dataclass



from expression import (

  MapApplication,

  MapSymbol,

)

from proof import (

  InferenceRule,
  PatternVariable,

  PremisePattern,

  Relation,

  RelationType,

)





@dataclass(frozen=True)

class InjectiveMapStatement:

  map: MapSymbol





@dataclass(frozen=True)

class IsomorphismStatement:

  map: MapSymbol





def isomorphism_implies_injective_inference_rule():
  map_variable = PatternVariable(name="map")

  def build_conclusion(
    premises,
  ):
    isomorphism_statement = (
      premises[0].conclusion
    )

    return InjectiveMapStatement(
      map=isomorphism_statement.map,
    )

  return InferenceRule(
    name="isomorphism implies injectivity",
    description=(
      "An isomorphism is injective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          IsomorphismStatement
        ),
        statement_pattern=IsomorphismStatement(
          map=map_variable,
        ),
      ),
    ),
    conclusion_pattern=InjectiveMapStatement(
      map=map_variable,
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )




def injective_map_reflects_equality_inference_rule():

  def guard(

    premises,

    bindings,

  ):

    injective_statement = (

      premises[0].conclusion

    )



    equality_relation = (

      premises[1].conclusion

    )



    if not isinstance(

      equality_relation.lhs,

      MapApplication,

    ):

      return False



    if not isinstance(

      equality_relation.rhs,

      MapApplication,

    ):

      return False



    return (

      equality_relation.lhs.map

      == equality_relation.rhs.map

      and injective_statement.map

      == equality_relation.lhs.map

    )



  def build_conclusion(

    premises,

  ):

    equality_relation = (

      premises[1].conclusion

    )



    return Relation(

      lhs=equality_relation.lhs.expression,

      rhs=equality_relation.rhs.expression,

      relation_type=RelationType.EQUALITY,

    )



  return InferenceRule(

    name="injective map reflects equality",

    description=(

      "If f is injective and "

      "f(a)=f(b), then a=b."

    ),

    premise_patterns=(

      PremisePattern(

        statement_type=(

          InjectiveMapStatement

        ),

      ),

      PremisePattern(

        statement_type=Relation,

        relation_type=(

          RelationType.EQUALITY

        ),

      ),

    ),

    conclusion_builder=(

      build_conclusion

    ),

    match_guard=guard,

  )


@dataclass(frozen=True)
class KernelZeroStatement:
  """A typed assertion that the kernel of the specified map is zero."""
  map: MapSymbol


@dataclass(frozen=True)
class ImageWholeStatement:
  """A typed assertion that the image equals the whole target."""
  map: MapSymbol


@dataclass(frozen=True)
class SurjectiveMapStatement:
  map: MapSymbol


def kernel_zero_implies_injective_inference_rule():
  """A homomorphism with zero kernel is injective."""
  from proof import PatternVariable

  group_map = PatternVariable(name="map")
  return InferenceRule(
    name="zero kernel implies injectivity",
    description="A group homomorphism with zero kernel is injective.",
    premise_patterns=(
      PremisePattern(
        statement_type=KernelZeroStatement,
        statement_pattern=KernelZeroStatement(map=group_map),
      ),
    ),
    conclusion_pattern=InjectiveMapStatement(map=group_map),
  )


def whole_image_implies_surjective_inference_rule():
  """A homomorphism whose image is its full codomain is surjective."""
  from proof import PatternVariable

  group_map = PatternVariable(name="map")
  return InferenceRule(
    name="whole image implies surjectivity",
    description="A group homomorphism whose image is its codomain is surjective.",
    premise_patterns=(
      PremisePattern(
        statement_type=ImageWholeStatement,
        statement_pattern=ImageWholeStatement(map=group_map),
      ),
    ),
    conclusion_pattern=SurjectiveMapStatement(map=group_map),
  )

@dataclass(frozen=True)
class ImageZeroStatement:
  """The image of this map is the zero subgroup."""
  map: MapSymbol


@dataclass(frozen=True)
class KernelWholeStatement:
  """The kernel of this map is its entire domain."""
  map: MapSymbol


def exactness_and_zero_image_implies_zero_kernel_inference_rule():
  """At an exact consecutive pair, zero image implies zero kernel."""
  from proof import ExactnessStatement, PatternVariable

  first_map = PatternVariable(name="first_map")
  second_map = PatternVariable(name="second_map")
  return InferenceRule(
    name="exactness and zero image imply zero kernel",
    premise_patterns=(
      PremisePattern(
        statement_type=ExactnessStatement,
        statement_pattern=ExactnessStatement(
          first_map=first_map, second_map=second_map, is_exact=True,
        ),
      ),
      PremisePattern(
        statement_type=ImageZeroStatement,
        statement_pattern=ImageZeroStatement(map=first_map),
      ),
    ),
    conclusion_pattern=KernelZeroStatement(map=second_map),
  )


def exactness_and_whole_kernel_implies_whole_image_inference_rule():
  """At an exact consecutive pair, a whole kernel implies a whole image."""
  from proof import ExactnessStatement, PatternVariable

  first_map = PatternVariable(name="first_map")
  second_map = PatternVariable(name="second_map")
  return InferenceRule(
    name="exactness and whole kernel imply whole image",
    premise_patterns=(
      PremisePattern(
        statement_type=ExactnessStatement,
        statement_pattern=ExactnessStatement(
          first_map=first_map, second_map=second_map, is_exact=True,
        ),
      ),
      PremisePattern(
        statement_type=KernelWholeStatement,
        statement_pattern=KernelWholeStatement(map=second_map),
      ),
    ),
    conclusion_pattern=ImageWholeStatement(map=first_map),
  )


def injective_and_surjective_imply_isomorphism_inference_rule():
    from proof import InferenceRule, PatternVariable, PremisePattern

    group_map = PatternVariable(name="group_map")
    return InferenceRule(
        name="injectivity and surjectivity imply isomorphism",
        description="A map which is both injective and surjective is an isomorphism.",
        premise_patterns=(
            PremisePattern(
                statement_type=InjectiveMapStatement,
                statement_pattern=InjectiveMapStatement(map=group_map),
            ),
            PremisePattern(
                statement_type=SurjectiveMapStatement,
                statement_pattern=SurjectiveMapStatement(map=group_map),
            ),
        ),
        conclusion_pattern=IsomorphismStatement(map=group_map),
    )
