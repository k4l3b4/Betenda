from django.db import transaction
from django.db.models import F
from Reactions.models import ReactionCount

def update_reaction_count(created, previous_reaction, reaction, content_type, object_id):
    try:
        with transaction.atomic():
            if created:
                try:
                    reaction_count = ReactionCount.objects.get(
                        reaction=reaction, content_type=content_type, object_id=object_id)
                    reaction_count.count = F('count') + 1
                    reaction_count.save()
                except ReactionCount.DoesNotExist:
                    ReactionCount.objects.create(
                        reaction=reaction, content_type=content_type, object_id=object_id, count=1)
            else:
                if previous_reaction:
                    try:
                        old_reaction_count = ReactionCount.objects.get(
                            reaction=previous_reaction.reaction, content_type=content_type, object_id=previous_reaction.object_id
                        )
                        if old_reaction_count.count <= 1:
                            old_reaction_count.delete()
                        else:
                            old_reaction_count.count = F('count') - 1
                            old_reaction_count.save()

                    except ReactionCount.DoesNotExist:
                        pass  # If previous_reaction does not exist, do nothing.

                try:
                    reaction_count = ReactionCount.objects.get(
                        reaction=reaction, content_type=content_type, object_id=object_id)
                    reaction_count.count = F('count') + 1
                    reaction_count.save()
                except ReactionCount.DoesNotExist:
                    ReactionCount.objects.create(
                        reaction=reaction, content_type=content_type, object_id=object_id, count=1)
    except Exception as e:
        print(f"Error updating reaction count: {e}")