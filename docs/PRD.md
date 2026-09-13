# Product Requirements Document

## AI Job Insight Assistant

| Item | Details |
|---|---|
| Product Type | AI-powered career analysis tool |
| Version | MVP 1.0 |
| Owner | ZHANG JIN |
| Status | In Development |
| Project Type | Personal Portfolio Project |

## 1. Product Background

Job descriptions often contain long, repetitive, and unstructured information. Candidates must manually identify role responsibilities, required skills, preferred qualifications, and business context before evaluating whether a position matches their experience.

This process becomes more difficult when candidates compare multiple roles across companies, such as product management, product operations, industry operations, business analysis, and strategy analysis.

The AI Job Insight Assistant aims to transform unstructured job descriptions into structured, actionable career insights.

## 2. Problem Statement

Target users currently face four major problems:

1. Job descriptions are lengthy and difficult to compare.
2. Important requirements are mixed with generic recruitment language.
3. Candidates struggle to connect their experience with specific job requirements.
4. Interview preparation is often generic rather than role-specific.

## 3. Target Users

### Primary Users

- University students applying for internships or graduate roles
- Candidates exploring product, operations, business analysis, and strategy roles
- Candidates comparing similar positions across multiple companies

### Secondary Users

- Career advisors
- University career service teams
- Early-career professionals considering a career transition

## 4. User Needs

| User Need | Product Response |
|---|---|
| Understand a job quickly | Extract and categorize key information |
| Judge personal fit | Match resume evidence with job requirements |
| Identify capability gaps | Generate a structured gap analysis |
| Compare multiple positions | Present role differences in a comparison view |
| Prepare for interviews | Generate role-specific interview questions |
| Protect personal data | Avoid storing resume content by default |

## 5. Product Goals

The MVP should help users:

- Understand a job description within three minutes
- Identify core responsibilities and skill requirements
- Match resume experience with individual requirements
- Discover missing skills and evidence
- Generate a practical interview preparation plan
- Compare job descriptions using a consistent framework

## 6. Non-Goals

The MVP will not:

- Make final application decisions for users
- Guarantee interview or recruitment outcomes
- Automatically submit job applications
- Fabricate resume experience
- Store personal resume information without permission
- Replace professional career advice

## 7. Core Features

### 7.1 Job Description Analysis

The user pastes a job description into the system.

The system extracts:

- Company and position name
- Role category
- Core responsibilities
- Required qualifications
- Preferred qualifications
- Business and industry keywords
- Tools and technical skills
- Leadership and collaboration requirements

### 7.2 Resume Matching

The user pastes resume content into the system.

For every job requirement, the system returns:

- Matching resume evidence
- Match strength
- Missing evidence
- Recommended improvement action

The system must not invent experience that is not contained in the resume.

### 7.3 Capability Gap Analysis

Requirements are classified into three categories:

- Strong Match
- Partial Match
- Capability Gap

The system explains why each requirement belongs to its category.

### 7.4 Interview Preparation

Based on the job description and resume, the system generates:

- Likely behavioral interview questions
- Likely business or case questions
- Resume deep-dive questions
- Suggested evidence for each question
- Areas requiring additional preparation

### 7.5 Multi-Role Comparison

Users can compare multiple positions based on:

- Role responsibilities
- Required skills
- Industry knowledge
- Data and technical requirements
- Leadership requirements
- Match level
- Preparation difficulty

This feature is planned for the second version.

## 8. User Flow

1. User opens the application.
2. User pastes a job description.
3. User optionally pastes resume content.
4. User selects an analysis mode.
5. The system processes the information.
6. The system displays structured results.
7. The user downloads or copies the analysis report.

### Analysis Modes

- JD Analysis
- Resume Matching
- Interview Preparation
- Multi-Role Comparison

## 9. Output Structure

The analysis report should include:

1. Position Overview
2. Core Responsibilities
3. Required and Preferred Qualifications
4. Business Keywords
5. Resume Evidence Mapping
6. Capability Gap Analysis
7. Interview Preparation
8. Recommended Next Actions

## 10. AI Design

### AI Responsibilities

The AI model is responsible for:

- Information extraction
- Requirement classification
- Semantic matching
- Explanation generation
- Interview question generation

### Structured Output

The model should return structured JSON rather than unrestricted text whenever possible.

Example:

```json
{
  "position": {
    "company": "",
    "title": "",
    "category": ""
  },
  "requirements": [
    {
      "requirement": "",
      "type": "required",
      "match_level": "strong",
      "resume_evidence": "",
      "gap": "",
      "recommendation": ""
    }
  ]
}
