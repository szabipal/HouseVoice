# Engineering Decisions

## Layered Backend

Routes and Telegram handlers stay thin. Services coordinate workflows, repositories handle persistence, and domain rules stay deterministic and easy to test.

## Privacy-Aware Inventory

Inventory can be `shared` or `private`. Recipe checks and meal logging use only inventory visible to the requesting user.

## AI Boundary

Receipt and recipe parsing live behind `app/llm` and `app/vision`. Model output must be validated before it mutates inventory.
