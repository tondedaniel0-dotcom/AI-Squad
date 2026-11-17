from models import ResultatVote, RevisionAgent, Vote


def organiser_vote(revisions: list[RevisionAgent]) -> ResultatVote:
    if not revisions:
        raise ValueError("Impossible d'organiser un vote sans révision d'agent.")

    roles = [revision.role for revision in revisions]
    if len(set(roles)) != len(roles):
        raise ValueError("Chaque agent doit avoir un rôle unique pour voter.")

    votes = []
    for revision in revisions:
        candidat = max(
            revisions,
            key=lambda proposition: (
                proposition.confiance,
                -len(proposition.objections),
                proposition.role,
            ),
        )
        votes.append(Vote(votant=revision.role, candidat=candidat.role))

    scores = {role: 0 for role in roles}
    for vote in votes:
        scores[vote.candidat] += 1

    score_maximal = max(scores.values())
    gagnants = [
        role for role, score in scores.items() if score == score_maximal
    ]

    return ResultatVote(
        votes=votes,
        scores=scores,
        gagnants=gagnants,
        taux_consensus=score_maximal / len(votes),
    )
