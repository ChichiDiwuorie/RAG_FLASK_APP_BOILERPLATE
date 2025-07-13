# MSFT AI-Genius-Challenge: RAG_FLASK_APP_BOILERPLATE

## Introduction
### Objective
Demonstrate that you can architect, secure, and ship a production-ready RAG workload on Azure. Success means your cloud resources are correctly wired, your AI assistant returns fact-based answers pulled from the provided document pack, and the automated evaluator (“MonitorEye”) awards a passing score for accuracy, performance, and deployment hygiene.
### Learning Tasks
You will (1) stand-up Azure storage and upload the evidence corpus, (2) create and tune an Azure AI Search index—including semantic or vector search, (3) deploy chat and embedding models in Azure OpenAI, (4) stitch retrieval + generation in a minimal API (Web App / Functions / Container App), and (5) expose an HTTPS endpoint that survives MonitorEye’s barrage of queries.
### Output
By the end you’ll have: an Azure resource group containing storage, search, OpenAI, and a publicly reachable inference endpoint; a working /ask API that accepts JSON { "question": "…" } and returns grounded answers; and lightweight documentation (README or inline help) summarising how to run, test, and clean up

---

## Step 1: Crisis Briefing
### ♦️ Stage 1: Scenario Briefing – Zero Day in Zero Hour
You’re an on-call engineer at Contoso Corp. At 03:00 UTC a sensitive web-gateway server, SVR-ACME-01, spiked in outbound traffic, crashed, and went dark. Forensics teams now believe a zero-day exploit is involved.
### Key Facts
Server affected: SVR-ACME-01 (runs the in-house ACME Web Gateway)
Observed anomalies:
• Sudden outbound data burst to an unknown IP
• Immediate CPU spike → crash
• Suspicious file + chunks of encrypted log data on disk
Clue found: text string “Blue Raven” inside a dropped file—unclear if real or a decoy
### Your Mission
Ingest evidence – Load every file in the Root-Cause Document Pack (incident reports, encrypted logs, attacker note, malware analysis) into Azure storage.
Index & retrieve – Use Azure AI Search to create a searchable/semantic index.
Augment & answer – Combine that index with an Azure OpenAI model so the LLM can answer questions with facts pulled from the documents.
Final objective – Produce a clear, evidence-backed answer to
“What was the root cause of the incident?”
### Why RAG?
Retrieval-Augmented Generation grounds an LLM’s responses in real data, sharply reducing hallucinations—vital when you’re reporting on cybersecurity breaches. Azure AI Search handles retrieval; Azure OpenAI handles generation.
### Scoring & Resources
No Azure resources are required yet; simply read and understand the scenario.
Ensure you’re signed into the managed Azure subscription provided for the AI Genius Challenge—work completed elsewhere won’t be graded.
A free-trial-level subscription is fine for personal testing, but only actions in the managed account count toward your score.
### Copilot Hint: As you proceed, you can ask Azure Copilot to summarize any document or clarify a step—but try to solve first, then verify with the Copilot to reinforce learning.
### Set Up Your Resource Group
A resource group is simply a tidy, logical container for everything you’re about to deploy—Storage, Azure AI Search, Azure OpenAI, and more. Keeping it all in one place makes both scoring and cleanup painless.
### Quick-Start Steps
Open Azure Portal → search Resource Groups → Create.
Pick your subscription, then name the group (e.g., rag-challenge-rg).
Choose a region that supports Azure OpenAI (East US, West Europe, etc.).
Review + Create → Create.
Copilot Tip: If you’re unsure which regions support OpenAI in your tenant, ask the Azure Copilot directly in the portal:
“List regions where Azure OpenAI is available for my subscription.”
### Naming Convention
Prefix with rag plus your initials or alias – e.g., rag-jm-rg.
Lowercase, 3-24 characters, no special symbols (Azure enforces it).
Using a predictable prefix speeds up automated scoring.
### Why It Matters
One-stop cleanup: when the challenge ends, delete the group and you’re done.
Automated detection: scoring scripts look for resources inside this group, so stray resources elsewhere won’t be counted.
Once your shiny new group appears (with zero resources inside), you’re ready to move on and start building in Stage 2.
terminal:
az group create -n rag-challenge-rg -l eastus

### ♦️ Stage 2: Prepare the Root-Cause Document Pack (This is optional – the Azure Portal is perfectly fine for this challenge.)
Before we build anything smart, we need to gather evidence — the digital breadcrumbs of the incident. The security team has provided a curated Root-Cause Document Pack, which includes the most critical traces left by the attacker. This will become the knowledge base that fuels our AI investigation.
### What’s Inside the Document Pack
You’ll soon upload these files to Azure Storage, but first, get a sense of what’s in the pack:
Initial Incident Report – the first response log describing the event timeline.
Encrypted Log File – suspicious machine data that might hide key IOCs.
Malware Analysis Summary – findings from reverse engineering the binary.
Ransom Note (False Flag) – likely a diversion tactic from the attacker.
Final Report Snippet – incomplete conclusions from an internal review.
These text-based artifacts represent ground truth — the verified (or at least observed) facts that we’ll later use to query and cross-check in our RAG pipeline.
### Why Azure Storage?
We’ll upload the document pack to an Azure Storage Account, which offers:
Global accessibility via HTTP/S
Unstructured data support (perfect for text, logs, PDFs, etc.)
Integration with Azure AI Search for indexing and retrieval
Scalable + cost-efficient for enterprise-grade workloads

---

## Step 2: Building the Knowledge Base
### ♦️ Stage 3: Provision the Azure Storage Account
To store your incident documents in a structured, queryable form, you’ll need an Azure Storage Account. Think of it as your digital evidence vault — everything else (AI Search, OpenAI, vector indexes) will reference this central store.
### Step-by-Step Guide: Creating the Storage Account
- Open Azure Portal: Search for “Storage Accounts” in the top search bar and click Create.
Basics Tab:
Subscription: Choose the same subscription you’ve been using.
Resource Group: Select the one created earlier (e.g., rag-challenge-rg).
Storage Account Name:
Must be globally unique, lowercase, and 3–24 characters long.
Avoid special characters or uppercase letters.
Naming tip: Use something like ragstorage<youralias> (e.g., ragstorageanita).
Region:
Match the region of your resource group (e.g., East US, West Europe).
Ensure this region supports Azure OpenAI and Azure AI Search (important for later stages).
Performance: Leave as Standard.
Redundancy (Replication): Choose Locally-redundant storage (LRS) — affordable and sufficient for this challenge.
### Click “Review + Create”
Confirm all settings and then click Create. Azure will deploy your storage account in under a minute.
### After Deployment
Navigate to the newly created storage account.
You’ll land on the Overview page — note down the Blob service endpoint and Storage account name (you’ll use them when configuring AI Search later).
### Best Practice Tip
All resources you create from this point onward should stay within the same resource group (rag-challenge-rg) and region. This ensures:
Lower latency (everything is nearby),
Easier cleanup (delete the RG when done),
Smooth validation (some challenge validators expect this structure).
Let’s move on and prepare the blob container for your document pack next.
Leverage Microsoft Copilot in Azure:
### Copilot Tip: How Azure Copilot Can Help You in Stage 3
While setting up your Azure Storage Account, Azure Copilot can act as your real-time assistant in the portal. Here's how it can help: 
* Explain concepts: Not sure what LRS or StorageV2 means? Just ask Copilot — it can provide context-specific definitions without leaving the portal.
* Guide you through UI steps: Ask “How do I create a storage account?” and Copilot will walk you through it, step by step, inside the Azure interface.
* Validate naming conventions: Copilot can verify if your naming aligns with Azure's requirements (e.g., lowercase, character limits) and suggest corrections before you hit an error.
* Recommend best practices: Unsure about replication types or region support? Copilot can suggest cost-effective defaults that work well for this challenge.
* Try typing in the Azure portal Copilot: “Help me create a storage account for RAG challenge” and let it guide your setup.

### ♦️ Stage 4: Set Up a Blob Container for Your Files
With your storage account in place, it’s time to create a Blob container — essentially a secure folder where you’ll upload all the incident documents. This container will serve as the foundation for indexing and search in later stages.
### Step-by-Step Guide: Creating the Blob Container
* Navigate to the Storage Account:
* In the Azure Portal, open your storage account (e.g., ragstoragejohn).
* In the left sidebar under Data storage, click Containers.
* Create a Container:
* Click + Container to add a new blob container.
* Name your container:
* Use lowercase letters, numbers, or hyphens.
* Must start and end with a letter or number.
* Good examples: documents, incidentdocs, or rootcausedata.
* Public access level:
* Select Private (no anonymous access).(This keeps your data secure and ensures only authenticated services like Azure AI Search can access it.)
Click “Create.”
Your Container is Ready
You should now see your new container in the list. Click on it — it will be empty initially. You’ll upload documents here shortly.
### Did You Know?
Blob containers are highly versatile:
They support REST APIs, SDKs, and tools like Azure Storage Explorer.
In enterprise use cases, you’d typically automate uploads using scripts, Logic Apps, or Azure Data Factory.
For this challenge, we’ll do a manual upload — simple, effective, and gets the job done.
Next up, we’ll populate this container with the Root-Cause Document Pack and prepare for indexing.
Leverage Microsoft Copilot in Azure:
### Copilot Tip: How Azure Copilot Can Help You in Stage 4
When you're setting up the blob container, Azure Copilot can assist you in streamlining and validating each action:
* Confirm container settings: Unsure about public access levels or naming rules? Ask Copilot, and it will explain acceptable patterns and recommend the most secure defaults (like "Private" access).
* Walk you through the creation process: Just ask something like “How do I create a private blob container in this storage account?” and Copilot will generate a guided walkthrough based on your current context.
* Security reminders: Copilot may prompt you about least-privilege best practices — reminding you that keeping containers private is ideal for enterprise workloads.
* Command generation: If you're curious about automating the same via CLI or ARM templates later, Copilot can even generate sample scripts on the fly.
* Try this in Copilot: “Show me how to create a blob container for uploading private incident files” and watch it walk you through the safest setup.
The following diagram shows the relationship between these resources.
The following diagram shows the relationship between these resources.

### ♦️ Stage 5: Upload the Root-Cause Document Pack to Azure Storage
You’ve got the container. Now it’s time to fill it with evidence. These documents will power your RAG pipeline by serving as the source of truth for incident investigation.
### Documents to Upload
You should have received a Root-Cause Document Pack – either as:
A set of individual .txt files, or
A single combined file that you’ll need to split into multiple parts.
If you're starting with a combined document, create five .txt files manually using any text editor, copying each section into its own file.
Recommended filenames:
* Doc1-IncidentBrief.txt
* Doc2-EncryptedLog.txt
* Doc3-MalwareAnalysis.txt
* Doc4-DecoyNote.txt
* Doc5-RootCauseReport.txt
 
💡 Tip: These filenames are referenced in later stages. Stick to this naming convention exactly to avoid any mismatch during scoring or automation.
 
🛠️ Upload Steps (Azure Portal)
 
Open your Blob Container (e.g., incidentdocs) inside the Storage Account.
Click the Upload button from the top menu.
In the Upload blade:
Click Browse and select the file(s) from your local machine.
You can upload all five files at once or one at a time.
Leave Blob type as Block blob and Access tier as Hot.
Click Upload. Wait for the process to finish.
Verify each file appears in the list with its name and size.
 
✅ Verify Content
 
After upload:
Click on each blob name to open its details pane.
Use the built-in preview to view the content (Azure will show text inline).
Confirm file integrity:
Doc2-EncryptedLog.txt should look unreadable — that’s okay.
Doc5-RootCauseReport.txt should contain some structured analysis or natural language text.
 
🔐 Best Practice (FYI)
 
In enterprise settings:
Sensitive documents should have restricted access.
Azure Storage supports Shared Access Signatures (SAS) and RBAC/Managed Identity for granular permissions.
For this challenge, we simplify it by allowing Azure AI Search to ingest using the account key.
 
📋 Scoring & Verification
 
The challenge platform may:
Count the number of blobs uploaded, or
Check for specific filenames.
To ensure credit:
Double-check that all 5 files are uploaded.
Match filenames exactly (e.g., RootCauseReport.txt, not rootcausereport.TXT or Doc5-report.txt).
 
🎉 You're Done!
 
You now have a fully populated knowledge base in Azure Storage.
Next up: indexing these documents with Azure AI Search to prepare them for intelligent retrieval.
This optional section provides extra context and tips about your storage setup.
 
You can use Azure Storage Explorer (a free Microsoft tool or via Portal's in-browser explorer) to manage and download/upload files easily, especially if dealing with many files. In this challenge, the Portal's upload is sufficient.
Azure Storage Account Keys: Azure Search (next stage) will need to read the files. The indexer can authenticate using the Storage account access key or a managed identity. Easiest for now: use the access key. Find it under your storage account’s Security + networking > Access keys. You don't need to do anything yet, but be aware where to get the connection string or key if needed. Copying the Connection string (which includes the key) is handy.
Cost Consideration: Storing a handful of text files costs almost nothing. Azure Storage billing is based on GBs stored and operations. This challenge’s data is minimal, so cost isn't a concern. Still, it’s good practice to delete the storage account after the challenge to avoid any lingering costs.
 
Did you know? You can mount Azure Blob storage as a drive in a VM or use it like a file system with tools. It’s very flexible for unstructured data. For now, our focus is on using it as a source for search indexing.

# Step 3: Indexing the Evidence
Azure Cognitive Search (recently also called Azure AI Search) is a fully managed search-as-a-service. First, we need to create the search service instance:
 
## Create Search Service: In the Azure Portal, click Create a resource and search for "Azure Cognitive Search" or "Azure AI Search". Select Azure Cognitive Search and click Create.
 
On the Create Azure Cognitive Search form (sometimes titled Create an Azure AI Search service):
 
Subscription & Resource Group: Use your challenge’s subscription and the resource group (e.g., rag-challenge-rg).
Service Name: Provide a name for your search service. It must be globally unique and only lowercase letters or numbers (similar to storage rules). For example, ragsearch<alias> (e.g., ragsearchjohn). The name will become part of your search endpoint URL (like https://ragsearchjohn.search.windows.net).
Location: Choose the same region as your other resources (consistency helps). Important: Not all regions support all features. Semantic search and vector capabilities are supported in certain regions. For example, semantic ranking is available in East US, South Central US, West Europe, etc.learn.microsoft.com. Ensure you select a supported region (the portal may indicate if a feature isn’t available in a region).
Pricing tier: Select a tier. For this challenge, if available, Free (F) tier might suffice (it allows 3 indexes, limited storage), but it may not support semantic features. If you need semantic search or vector, choose Basic or Standard S tier. Basic is a cost-effective choice that supports semantic queries with a limitlearn.microsoft.com. (Standard tiers support more storage and replicas; for a small dataset, Basic is fine).
Leave other settings (like availability zones, etc.) default unless required.
 
Review and Create the service. It may take a minute or two to deploy.
 
Once deployed, navigate to the search service’s page. Take note of the URL endpoint and Admin API Keys (under Keys section) – we’ll need the key to query or index via APIs. The portal provides Query keys and Admin keys; the Admin key is needed for indexing operations.
 
Tip: You can try Azure AI Search for free – each subscription can have one free search servicelearn.microsoft.com. If using the free tier, note it has limits (only 1 replica, small index limit) and Microsoft may delete it if inactivelearn.microsoft.comlearn.microsoft.com. Because our data is small, free tier should work if available.
Publicly accessible endpoint for the RAG
Azure Cognitive Search provides an Import data wizard that can connect to your Azure Blob container and create an index, data source, and indexer for youlearn.microsoft.com. We will use this portal wizard to quickly ingest our documents from Stage 2.
 
## Steps to Index Data:
In your search service’s Azure Portal page, find the Import data button (often on the Overview or Indexes tab). Click Import data to launch the wizard.
 
Data source: Choose Azure Blob Storage as the data source type. You’ll be prompted to connect to your storage:
Select the subscription and the storage account you created in Stage 2.
Enter the container name (e.g., incidentdocs). The wizard might list containers to pick from.
Authentication: Choose to enter connection credentials. You can use the storage connection string (from Stage 2.4) or select "resource identity" if you want to use managed identity. For simplicity, use the connection string method:
You might need to paste the connection string from the Access keys blade of the storage account.
Test connection if option is available, then proceed.
 
Configure Index: The wizard will propose an index name and fields. You can name the index (e.g., incidents-index or rag-index). It will detect the blob content is text and likely suggest a field like "content" and metadata fields (like metadata_storage_path, etc.).
 
Accept defaults for field mappings. Ensure content or content_text field is included (this contains your file text). Also enable the key field (usually id or metadata_storage_path gets marked as key).
If there’s an option, enable Semantic settings or Semantic ranking by creating a semantic configuration. (This might not appear in the wizard; you may add it later via the portal by defining a semantic config on the index if needed.)
If the wizard allows, you might also enable vectorization (some newer versions have an “Import and vectorize” optionlearn.microsoft.comlearn.microsoft.com). We will address vector indexing in the next section, so it’s okay if we just do a basic text index now.
 
Indexer settings: Give the indexer a name (e.g., blob-indexer) and choose whether to run it once or schedule (default is once now, which is fine). The indexer is what actually pulls data from storage into the index.
 
Click Submit to start the indexing process.


The portal will create:
A Data Source pointing to your storage/container.
An Index in your search service with fields for content and metadata.
An Indexer that runs and loads the data.
After a short time (a few seconds for our small data), you should see the indexer status as successful and documents count reflecting the number of files (it should say, for example, 5 documents successfully indexed if you uploaded 5 files).
 
Verify the Index Content: Use Search Explorer in the portal (usually available on the index page or the search service overview). Select your index and try out some search queries:
For example, search for "exploit" or "Blue Raven" or a keyword known to be in one of the docs. The search explorer will return matching documents with some snippet of text. This confirms your index is working and contains the content.
Try a keyword from the encrypted log (which might not yield results, since it's random text – a good thing to note).
Try a term you expect in the final report like "root cause" or "SVR-ACME-01" to see if the relevant doc comes up.
 
If semantic search is enabled, the Search Explorer may allow a toggle for semantic answers (if your tier supports it). It can return a summarized answer, but even if not, we will handle summary via OpenAI later.
To enhance retrieval, we want to go beyond simple keyword search:
 
Semantic Search: This uses AI to interpret the query's meaning and rank search results by relevance, even if wording differslearn.microsoft.com. It's great for natural language questions.
Vector Search: This involves using embeddings (numerical representations of text) to find similar content. It’s useful when exact keywords don't match, e.g., finding relevant info for "unknown malware" even if those exact words aren’t in documents. Azure Cognitive Search supports vector fields and integrated embedding generation with Azure OpenAI.
 
Enable Semantic Ranking: If your search service tier supports it (Basic or above):
In the Azure portal, go to your index and look for Semantic settings. You may create a semantic configuration by choosing which fields are content (e.g., the "content" field) and title/keywords (if any). Name the config (e.g., default-semantic) and save.
This allows you to add queryLanguage=en-us&queryType=semantic&semanticConfiguration=default-semantic in queries to get semantic ranking and even summary answers (if using the REST API or SDK).
There’s no cost to enable, but semantic queries have a limit count per service per day (should not be an issue in our scenario usage)learn.microsoft.com.
 
Set Up Vector Index (optional but powerful): This part is advanced and optional depending on the challenge level. To truly implement RAG, we can incorporate vector similarity:
 
Azure AI Search now offers an Import and Vectorize wizard that integrates with Azure OpenAI to generate embeddings during indexinglearn.microsoft.comlearn.microsoft.com. This requires an Azure OpenAI embedding model deployment (which we'll do in Stage 4).
 
If you want to add vector search now, you can rerun the indexing using the new wizard:
 
Ensure you have an embedding model ready (if not, skip and do this after Stage 4).
In your search service, click Import and vectorize data (if available). It’s similar to the import data wizard but adds steps to choose an embedding model.
Connect to the same data source (your blob container).
When prompted for Vectorize your content (embedding), choose Azure OpenAI as the model source, then select the deployment name of an embedding model (e.g., text-embedding-ada-002 which we'll create in Stage 4). You might need to provide the Azure OpenAI resource details and key or use managed identity if in the same tenant.
The wizard will automatically chunk documents if needed and create a new index with a vector fieldlearn.microsoft.comlearn.microsoft.com. For example, it may create a field like @search.embedding that holds the vector for each document chunk.
Complete the wizard to create a new index (say incidents-index-vector).
After indexing, each doc (or chunks of docs) now has vector embeddings stored. You can query this index by sending a vector in the query (we’ll do that in code in Stage 4/5).
 
Alternatively, if the portal wizard is not available or you prefer code: you could manually add a vector field to your existing index and call the Azure OpenAI embedding API for each document, then push those vectors via the Search REST APIleazrn.microsoft.comlearn.microsoft.com. This is more involved, so using the wizard or ignoring vector for now is acceptable.
 
Note: Even without vector search, the combination of keyword + semantic search is usually sufficient for our small scenario. However, vector search shines when questions are phrased differently than the docs. For example, our docs might say "intrusion used a previously unknown exploit", and a question might be "was a zero-day used?". A vector search could match those semantically. We will demonstrate using embeddings at query time in the next stage.

# Step 4: Empowering the AI – Azure OpenAI Integration

Azure OpenAI Service gives you access to powerful language models (like GPT-3.5 Turbo, GPT-4, and Ada for embeddings) via Azure. Creating this resource requires special access (you must have an approved application for OpenAI usage). Assuming you have access:
 
## Create Resource: In Azure Portal, click Create a resource and search for "Azure OpenAI". Select Azure OpenAI Service and click Create.
 
On the Basics tab of the Create form, fill in:
Subscription & Resource Group: Use the same ones for consistency (rag-challenge-rg).
Region: Select a region that supports Azure OpenAI (at the time of writing, regions like East US, South Central US, West Europe, etc., support it – the portal will list allowed regions). This must be one of the approved regions and ideally the same region as your Cognitive Search if you plan to use integrated vectorization (the vector index wizard required the search and OpenAI to be in the same region for managed identity accesslearn.microsoft.comlearn.microsoft.com).
Name: Give your OpenAI resource a name, e.g., rag-openai.
Pricing Tier: Only Standard is available currently for OpenAI.
 
On the Management tab, you might need to confirm or select certain details (like the resource will be accessible via REST API, etc.). Usually, defaults are fine.
 
Review + Create and then Create. Deployment may take a minute.
 
Once deployed, open the Azure OpenAI resource. This resource itself is like a container for model deployments. By default, it has no models deployed.
With the Azure OpenAI resource ready, the next step is to deploy the specific models we’ll use:
 
Chat Completion model: e.g., gpt-35-turbo (which is GPT-3.5 Turbo) or gpt-4 if available. This will be used to generate answers using retrieved data.
Embedding model: e.g., text-embedding-ada-002. This will be used to convert text to vectors for semantic similarity search.
 
Deploy a Chat Model (GPT):
 
In the Azure OpenAI resource blade, find Model deployments (or there might be a Deployments tab).
 
Click + Create or Deploy a model.
Choose a Model: Select GPT-3.5-Turbo (versions might be labeled with an edition, choose latest stable).
Model name: The system might prefill ID like gpt-35-turbo. You can give a custom deployment name. For example, gpt35 or chat-model. This is the name your application will refer to when making API calls.
Scale: default is fine (you can often only choose 1 replica for now).
 
Click Deploy. It will take a short time (15-30 seconds typically) to deploy the model. Once done, you’ll see it in the deployments list with status “Succeeded” and “In Service”.
 
Deploy an Embedding Model:

4. Again click + Create to deploy another model.
Choose model: Select text-embedding-ada-002 (this is a popular embedding model for text).
Deployment name: e.g., text-embed-ada or simply ada-embed.
Deploy it similarly.
 
Confirm both models are deployed and Available.
 
Now you have two endpoints within the same OpenAI resource: one for chat completions and one for embeddings. You can view each deployment’s details, like name, model, and object ID.
 
Azure OpenAI Studio: You can also open Azure OpenAI Studio (link available on the resource page) to test the models:
 
Go to OpenAI Studio, select your resource and deployment. For the chat model, try the Chat Playground: you can enter a prompt. For example, “Hello, how do I use RAG?” and see it respond. This just tests the model is working.
For the embedding model, there's no direct chat, but you could use the REST API or Python to test.
 
Tip: The Keys and Endpoint for your OpenAI resource are needed for API calls. On the Azure OpenAI resource page, under Keys and Endpoint, copy the Endpoint URL (e.g., https://your-resource-name.openai.azure.com/) and one of the keys (key1 or key2). We'll use these in our application to call the OpenAI API.

Best Practice: Treat these keys like secrets – don't expose them publicly. We'll later show how to keep them in app settings or Azure Key Vault.

Scoring: The challenge may verify that you have at least one deployment of a completion model and possibly an embedding model. It might check via the resource's properties or simply require a certain model name. To be safe, ensure at least the chat model is deployed with a known name (some challenges expect "gpt-35-turbo" deployment). If specified, follow the exact naming instructions for deployments. With models in place, we can combine search and OpenAI to complete the RAG pipeline.
Now comes the heart of RAG: combining the search results with the LLM. There are a few patterns to implement this:
 
Search then Prompt: Take the user’s question, use it to query the search index, get back top relevant document snippets, and feed those snippets into the prompt for the GPT model to generate an answer with references.
Embedding-based retrieval: Convert the question to an embedding (with Ada), use that vector to query the index for similar content (if vector index set up), then feed results to GPT.
Hybrid: possibly use both keywords and embeddings for robust retrieval (out of scope for now).
 
We will implement pattern (1) and (2) in concept. This section is more about formulating the approach and perhaps writing a local test code snippet. In Stage 5, we’ll integrate this into a deployed app.
 
Formulate the Prompt: We want the AI to use the documents, not just its own knowledge. A common prompt structure:
 
"You are a cybersecurity assistant. Use the information provided to answer the question. 
Context: <<document excerpts>>
Question: <<user question>>
Answer in detail using the context, and cite the document names if relevant."

This way, the model knows to ground its answer in the context we supply.
 
Steps to Perform RAG Query (Pseudo-code):
 
User Question: e.g., "What was the root cause of the incident?"
 
Search the Index: Use Azure Cognitive Search REST API or SDK to search the incidents-index. For example, via REST GET:
GET https://<search-service>.search.windows.net/indexes/incidents-index/docs? api-version=2021-04-30-Preview &search="root cause incident"&queryType=semantic&semanticConfiguration=default-semantic&$top=3
(with appropriate headers including api-key). This would retrieve the top 3 documents with semantic rankinglearn.microsoft.com. Alternatively, use queryType=full for regular search. If using vector:
First get embedding of question: call OpenAI embedding endpoint with the question text, get embedding vector.
Then call search POST query with { "vector": { "value": [embedding array], "fields": "content_vector", "k": 3} } to get top 3 by vector similarity.
 
Retrieve Results: The search response contains documents (likely our original text). Extract the most relevant sections. If the docs are long, maybe truncate to a few paragraphs that matched (the response often includes highlights or the content field).
 
Construct Prompt: Insert the retrieved text into a system or user message for the chat model. E.g.:
system_message = "You are a helpful assistant for incident investigation." user_message = f"Here are some documents:\n{doc1}\n{doc2}\n{doc3}\nUsing this information, answer the question: {user_question}. If the answer is not in the documents, say you don't know. Provide references."
(Alternatively, use the OpenAI Chat API with role "user" containing both context and question, or use a single completion prompt if not using chat format.)
 
Call OpenAI Completion: Use the Azure OpenAI REST API for the chat model. For example:
POST https://<openai-resource>.openai.azure.com/openai/deployments/<chat-model>/chat/completions?api-version=2023-03-15-preview { "messages": [ {"role": "system", "content": "You are ... (instructions)"}, {"role": "user", "content": "Here are docs... Question: ..."} ], "temperature": 0, "max_tokens": 500 }
(The exact endpoint and API version might differ; check Azure OpenAI docs.)
 
Get Answer: The response will have the assistant’s answer. Ideally, it will mention the root cause and maybe cite the context. We can post-process if needed (e.g., ensure it mentions a specific document as reference).
 
Return Answer: This answer can be shown to the user, completing the cycle.
 
In practice, you'd adapt this to the language of your choice or use SDKs:
Azure Search SDK (for example, Azure SDK for Python azure-search-documents) can query the index.
Azure OpenAI can be called via the OpenAI Python library by configuring api_type Azure, or simply via requests as above.
 
Test Locally (if possible): If you have a development environment, test a known question. For example, ask: "What is Blue Raven?" or "What was the exploit used?" and see if it finds the relevant doc. If not feasible to run code here, we'll test once deployed.

Best Practices & Tips:
Keep temperature low (0.0–0.3) for deterministic, factual answers in this scenario. We want accurate answers, not creative ones.
Use prompt engineering to instruct the model clearly to use the provided documents and not make things up. E.g., we said "If the answer is not in the documents, say 'I don't know'" to handle unknowns.
Limit the size of each document in the prompt if they are large. You can truncate or summarize them before feeding to GPT to avoid hitting token limits.
Azure OpenAI has rate limits and quotas. Our usage is small (one question at a time), but be mindful in a multi-user or repeated query scenario.
Did you know? You can also use tools like LangChain or Azure OpenAI Studio's Playground with your data to simplify RAG. But here, we implement it ourselves for learning.
Before deploying, let's cover a few important considerations to do this responsibly:
 
Keys and Secrets: We have two sensitive keys: the Search API key and the OpenAI API key. In development code we showed them as variables, but in deployment, do not hardcode them. We will use Azure App Service settings to store these or Azure Key Vault. Plan to retrieve them from environment variables in your app (e.g., os.environ['OPENAI_KEY']). This way, you can rotate or manage them without code changes.
 
Cost Awareness: Azure OpenAI charges per 1K tokens. Our prompt plus answer might be a few hundred tokens per question, which is negligible for a few queries. But if you test many times or allow free-form queries, keep an eye on usage. The search service is billed per indexing and query operation, but cost is minimal for low usage (and free tier is free up to certain limits).
 
Content Filtering: Azure OpenAI has built-in content filters. In a cyber incident context, this likely won't trigger, but if any document or query had very sensitive or unsafe content, the model might refuse to answer or log a content filter event.
 
Semantic vs Vector vs Hybrid: For completeness, note that with the embedding model deployed, you could integrate the embedding approach. For instance, use the embedding model to vectorize both documents (done in Stage 3 vector index) and queries (real-time via API). This often improves finding relevant context, especially if wording differs. If time permits, consider testing both approaches in your code. (One could even do: use search with the question directly, and use vector search with embeddings, then merge results.)
 
Testing: Try a couple of queries manually by calling your logic before deployment. For example, you might run the above code in a Notebook or local script with a sample question like "What does the encrypted log reveal?" and see if the answer makes sense.
 
Having set up both Search and OpenAI, you have all pieces needed for RAG. The last step is to deploy this as a web application or API that can be accessed as part of the gamified challenge (so that the evaluation agent or user can interact with it).


# Step 5: Deployment – Bringing the Solution to Life

[RESOURCE_PROVISIONING]
READY
Azure resources have been successfully provisioned. You can proceed to the next step.

Name: rag-wb01-cdi
Type: Microsoft.Web/sites
Location: eastus
🚀 Deploy Your Flask / FastAPI App to Azure App Service with VS Code
Having deployed Azure AI Search, and a Chat Completion model using the AI Foundry -- now you need to make the RAg available via REST-APIs for applications to query and make the intelligence accessible.
Goal - Create Flask App (Code provided under resource(s) section), Set the secrets, and ship it to a live Azure Web App—all without leaving VS Code.
🛠 Prerequisites
✔	Tool	Notes
🖥	VS Code + Azure Tools extension pack	Bundles App Service, Azure CLI, Azure Account…
🐍	Python 3.9 + & Git	Installed locally
☁️	Azure CLI (az)	Run az login once—VS Code re-uses the token
 
 
 
1️⃣ Download the Starter Code 📦
Go to the Resources tab in this workbook.
Download Boilerplate Code [RAG] ZIP File.
Extract it → open the folder in VS Code:
cd path/to/extracted
code .
The project already contains requirements.txt, and app.py (The FLask App you need)
 
 
2️⃣ Identify Environment Variables 🔑
Peek into code for secrets / environement variables like - available from the previous stages / deployments made during those stages.
OPENAI_API_KEY, VECTOR_STORE_URL, AZURE_COSMOS_KEY, etc.
Do not commit secrets—keep them handy for the next step.
 
 
3️⃣ Create the Web App from VS Code ☁️
Click the Azure icon (Activity Bar).
Under RESOURCES, right-click your subscription → Create Resource… → Create App Service Web App…
Fill the wizard:
App name: rag-wb01-<your-initials> (must be globally unique)
Runtime stack: Python 3.13 (Linux)
Plan: Basic B1 (perfect for workshops, low cost)
VS Code provisions the Resource Group, App Service Plan, and Site automatically. 🪄
 
 
4️⃣ Add Environment Variables 📝
Method	Steps
A. VS Code 🧩	1. In Azure panel, right-click the new app → Application Settings → Add New Setting.2. Enter each key-value from .env.3. Hit the 💾 Save icon.
B. Azure Portal 🌐	Portal → App Service → Settings › Configuration → + New application setting.Save → Confirm restart.
 
 
 
5️⃣ Deploy the Code 📤
Still in VS Code, right-click the app → Deploy to Web App…
Select your project folder. VS Code zips, uploads, restarts.
When prompted “Update build configuration for Python?” 👉 choose Yes.
 
 
6️⃣ Verify & Stream Logs 🔍
After “Deployment Complete” toast, click Browse Website → https://<app-name>.azurewebsites.net.
Blank page? In Azure panel: right-click app → Start Streaming Logs to view real-time stdout / errors.
 
 
7️⃣ Clean-up After the Lab (Optional) 🧹
In Azure panel, right-click the Resource Group → Delete Resource Group… → confirm.
This removes the Web App & plan, preventing surprise costs.
 
💡 Key Take-aways
 	 
🔧	The workbook’s code is cloud-ready—App Service auto-detects Flask/FastAPI (no Dockerfile required).
🔐	Secrets stay in App Settings, never in source control.
🎯	Azure Tools for VS Code streamline everything: create → configure → deploy → live-log—all inside the editor.


Step 6
The Evaluation-Agent Challenge

Your RAG pipeline now faces one definitive question from the incident-response board:
“What was the root cause of the incident?”
1 | How to approach the problem - here're some helpful way to think on the lines - allowing you to challenge your RAG!
Requirement	Guidance
Primary finding	Pin-point the exact previously-unknown vulnerability (e.g., a zero-day in a critical gateway or service), and describe how it opened the door—typically via remote-code execution (RCE) or a comparable control-takeover.
System impacted	State the first asset compromised (server, container, device, etc.) using the identifier found in the briefs.
Attack method	Summarise the adversary’s initial foothold (e.g., unauthorised RCE), and the immediate actions they performed (malware drop, log tampering, data exfiltration, etc.).
Evidence	Quote or paraphrase the relevant passages from the official Root-Cause Analysis document—and, if helpful, cross-reference corroborating briefs.
Signal over noise	Exclude red herrings (decoy ransom notes, misleading artefacts) and keep the answer concise—no more than ~300 words.
Example outline (do not copy verbatim)
“The breach originated from a previously unknown Blue Raven zero-day in the ACME web gateway. Exploiting it, attackers obtained RCE on SVR-ACME-01, installed log-wiper malware, and pivoted to steal data.”
 
2 | How the grading works
TruthSeeker, an unbiased AI agent, hits your API every 30 seconds. It:
Sends the question to your deployed endpoint - from the previous stage.
Performs a semantic comparison of the returned answer against preshared ground-truth passages from the briefing set.
Logs pass/fail signals for final scoring at the workbook deadline.
 
3 | Developer checklist before submission
Endpoint live – confirm curl returns HTTP 200 with a substantive body.
Env-vars – verify keys (e.g., OPENAI_API_KEY) are set on Azure App Service.
Manual smoke test – query your app and confirm the response meets all items in §1.
Iterate quickly – you can redeploy, swap models, or tweak context windows anytime before the deadline; TruthSeeker will re-evaluate automatically.
 
4 | Scoring rubric (automated)
Keyword presence Do not worry on these lines, as the evaluation is semantic by nature - as long as the answer lise in neighbourhood to your RAG's response - you score!
Semantic match Content aligns with Document 5 facts
Clarity & length Human-readable, ≤ 300 words
 
Meet every bullet, and your RAG pipeline passes its ultimate trial. The crisis-response board—and TruthSeeker—are watching. 🎯
Submit Your Model

Submission

http://127.0.0.1:5000

<img width="407" alt="image" src="https://github.com/user-attachments/assets/8efe782b-ab05-4e0a-bb95-7d28465753b8" />
