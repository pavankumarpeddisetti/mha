/**
 * Type definitions for API responses
 * These match the backend Pydantic models
 */

/**
 * @typedef {Object} OCRData
 * @property {string} name
 * @property {string} course
 * @property {string} issuer
 * @property {string} date
 * @property {string} certificate_id
 * @property {string} raw_text
 */

/**
 * @typedef {Object} MetadataData
 * @property {string} created_date
 * @property {string} modified_date
 * @property {string} author
 * @property {string} software
 * @property {string[]} flags
 */

/**
 * @typedef {Object} QRData
 * @property {boolean} found
 * @property {string} content
 * @property {'valid'|'invalid'|'unverifiable'} validation
 */

/**
 * @typedef {Object} LogoMatch
 * @property {string} name
 * @property {number} confidence
 */

/**
 * @typedef {Object} LogoDetectionData
 * @property {LogoMatch[]} matches
 * @property {boolean} flag
 */

/**
 * @typedef {Object} TamperReport
 * @property {number} score
 * @property {string} heatmap - base64 encoded image
 */

/**
 * @typedef {Object} TrustEvaluation
 * @property {number} trust_score
 * @property {'Valid'|'Suspicious'|'Fake'|string} verdict
 * @property {string[]} reasons
 */

/**
 * @typedef {Object} CertificateAnalysisResponse
 * @property {string} certificate_preview - base64 encoded PNG
 * @property {OCRData} ocr
 * @property {MetadataData} metadata
 * @property {QRData} qr
 * @property {LogoDetectionData} logo_detection
 * @property {TamperReport} tamper_report
 * @property {TrustEvaluation} trust_evaluation
 */

export {}

